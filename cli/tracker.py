""" Deterministic application-tracker access. """

import os
import re
import zipfile
from datetime import date, datetime
from pathlib import Path
from typing import cast

import openpyxl
from openpyxl.utils import column_index_from_string, get_column_letter
from openpyxl.utils.exceptions import InvalidFileException
from openpyxl.worksheet.worksheet import Worksheet

TRACKER_PATH = Path("tracker.xlsx")

CELL_REF = re.compile(r"[A-Z]{1,3}[1-9][0-9]*")
ISO_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")


class TrackerError(Exception):
    """ Tracker file missing, unreadable, or an edit was refused. """


def _fmt(value: object) -> str:
    """ Render a cell value for a markdown table cell: ISO dates, blanks empty,
    pipes and newlines escaped so a cell can't break the table. """
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return str(value).replace("|", "\\|").replace("\n", " ")


def _sheet_markdown(ws: Worksheet, grid: bool = False) -> str:
    rows = [[_fmt(v) for v in row] for row in ws.iter_rows(values_only=True)]
    while rows and not any(rows[-1]):  # Excel pads its used-range with styled-but-empty rows
        rows.pop()
    if not rows:
        return f"## {ws.title}\n\n(empty)"

    if grid:  # sheet row numbers + column letters, for cell addressing
        header = ["#", *(get_column_letter(i) for i in range(1, len(rows[0]) + 1))]
        body = [[str(n), *row] for n, row in enumerate(rows, start=1)]
    else:
        header, *body = rows

    lines = [
        f"## {ws.title}",
        "",
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(["---"] * len(header)) + " |",
        *("| " + " | ".join(r) + " |" for r in body),
    ]
    return "\n".join(lines)


def read_tracker(path: Path = TRACKER_PATH, grid: bool = False) -> str:
    """ Dump every sheet of the tracker workbook to faithful markdown.

    Structure-agnostic: assumes nothing about columns, header rows, or sheet count.
    Interpretation is left to the reader. Raises TrackerError when the file is absent. """

    wb = _load(path, data_only=True)
    return "\n\n".join(_sheet_markdown(ws, grid=grid) for ws in wb.worksheets)


def _coerce(raw: str) -> object:
    """ Deterministic typing: empty clears, ISO dates become datetimes, numerics become numbers. """
    if raw == "":
        return None
    if ISO_DATE.fullmatch(raw):
        try:
            return datetime.strptime(raw, "%Y-%m-%d")
        except ValueError:
            raise TrackerError(f"{raw!r} is shaped like a date but isn't a valid one")
    if re.fullmatch(r"[+-]?[0-9]+", raw):
        return int(raw)
    if re.fullmatch(r"[+-]?[0-9]*\.[0-9]+", raw):
        return float(raw)
    return raw


def _list_options(dv: object) -> list[str] | None:
    """ The options of an inline list validation, else None. The one parser of the xlsx
    dropdown-formula grammar, shared by enforcement and schema description. """
    formula = getattr(dv, "formula1", None)
    if getattr(dv, "type", None) != "list" or not formula:
        return None
    if not (formula.startswith('"') and formula.endswith('"')):
        return None
    return [option for option in formula[1:-1].split(",") if option]


def _check_validations(ws: Worksheet, coord: str, raw: str) -> None:
    """ Enforce the sheet's own inline list validations (the dropdowns the user
    maintains in Excel/Numbers). Other validation types are left to the apps.
    Clearing is always allowed: a dropdown restricts entered values, not absence. """
    if raw == "":
        return
    validations = cast("list", ws.data_validations.dataValidation)  # openpyxl descriptor confuses ty
    for dv in validations:
        allowed = _list_options(dv)
        if allowed is None or coord not in dv.sqref:
            continue
        if raw not in allowed:
            raise TrackerError(f"{coord}: {raw!r} is not in the cell's dropdown {allowed}")


def _column_date_format(ws: Worksheet, column: int) -> str | None:
    """ The column's existing date convention, if it has one. """
    for (cell,) in ws.iter_rows(min_col=column, max_col=column):
        if isinstance(cell.value, (datetime, date)) and cell.number_format != "General":
            return cell.number_format
    return None


def _dropdowns(ws: Worksheet) -> dict[str, list[str]]:
    """ Column letter -> allowed values, from the sheet's inline list validations. """
    allowed_by_column: dict[str, list[str]] = {}
    validations = cast("list", ws.data_validations.dataValidation)  # openpyxl descriptor confuses ty
    for dv in validations:
        if (allowed := _list_options(dv)) is None:
            continue
        for rng in dv.sqref.ranges:
            for col in range(rng.min_col, rng.max_col + 1):
                allowed_by_column[get_column_letter(col)] = allowed
    return allowed_by_column


def _header_row(ws: Worksheet) -> tuple[int, dict[str, str | None]]:
    """ The first non-empty row is the header row — the one structural assumption the
    row verbs make. Returns (row number, header name -> column letter). A header that
    appears on several columns maps to None, so resolution refuses it instead of
    silently writing to whichever column came last. """
    for row in ws.iter_rows():
        cells = [
            (str(cell.value).strip(), cell.column_letter)
            for cell in row
            if cell.value is not None and str(cell.value).strip()
        ]
        if cells:
            headers: dict[str, str | None] = {}
            for name, letter in cells:
                headers[name] = None if name in headers else letter
            return row[0].row, headers
    raise TrackerError(f"sheet {ws.title!r} is empty: no header row to key against")


def _resolve_header(headers: dict[str, str | None], name: str) -> str:
    """ Header name -> column letter, case-insensitively. Unknown names fail loudly
    with the real headers, so a caller never needs prior knowledge of the columns. """
    matches = [letter for display, letter in headers.items() if display.lower() == name.strip().lower()]
    if not matches:
        raise TrackerError(f"no column {name!r}; headers are: {', '.join(headers)}")
    if len(matches) > 1 or matches[0] is None:
        raise TrackerError(f"{name!r} is ambiguous: several columns share that header; address cells with `set`")
    return matches[0]


def _next_row(ws: Worksheet, header_row: int) -> int:
    """ The row after the last occupied one. Appends land at the true end of the table,
    never in an interior blank left by a cleared-out entry, and past whatever
    styled-but-empty rows Excel pads the used range with. """
    last = header_row
    rows = ws.iter_rows(min_row=header_row + 1, values_only=True)
    for n, values in enumerate(rows, start=header_row + 1):
        if any(v is not None for v in values):
            last = n
    return last + 1


def _match_rows(ws: Worksheet, needle: str, header_row: int) -> list[tuple[int, str]]:
    """ Rows where any cell contains `needle`, case-insensitively. Returns (row number,
    preview) pairs for unambiguous selection and helpful error listings. """
    found: list[tuple[int, str]] = []
    rows = ws.iter_rows(min_row=header_row + 1, values_only=True)
    for n, values in enumerate(rows, start=header_row + 1):
        if any(v is not None and needle.lower() in str(v).lower() for v in values):
            preview = " | ".join(_fmt(v) for v in values if v is not None)
            found.append((n, preview[:120]))
    return found


def _split_assignment(assignment: str) -> tuple[str, str]:
    """ 'KEY=VALUE' -> (KEY, VALUE), splitting on the first '='. Values that would
    become formulas are refused here, once, for every write verb. """
    key, eq, raw = assignment.partition("=")
    key = key.strip()
    if not eq or not key:
        raise TrackerError(f"expected KEY=VALUE, got {assignment!r}")
    if raw.startswith("="):
        raise TrackerError(f"{key}: a value starting with '=' would become a formula; refusing")
    return key, raw


def _load(path: Path, data_only: bool = False) -> openpyxl.Workbook:
    """ The one open path: a missing file gets the bootstrap hint, an unreadable one a
    clean error, for every verb alike. """
    if not path.exists():
        raise TrackerError(f"no tracker at {path} (copy tracker.xlsx.example to {path} to start)")
    try:
        return openpyxl.load_workbook(path, data_only=data_only)
    except InvalidFileException as exc:
        raise TrackerError(f"{path} is not a readable xlsx ({exc})") from exc


def _open_for_write(path: Path) -> openpyxl.Workbook:
    """ `_load` for a round-trip-safe edit: formulas kept intact (never data_only), and
    workbooks with charts/images refused — the one thing an openpyxl save silently drops. """
    if path.exists():
        with zipfile.ZipFile(path) as zf:
            if any(n.startswith(("xl/media/", "xl/charts/", "xl/drawings/")) for n in zf.namelist()):
                raise TrackerError(
                    f"{path} contains charts/images, which an openpyxl save silently drops; "
                    f"make this edit in Excel/Numbers instead"
                )
    return _load(path)


def _sheet(wb: openpyxl.Workbook, sheet: str | None, path: Path) -> Worksheet:
    if sheet and sheet not in wb.sheetnames:
        raise TrackerError(f"no sheet {sheet!r} in {path} (has: {', '.join(wb.sheetnames)})")
    ws = wb[sheet] if sheet else wb.active
    if ws is None:
        raise TrackerError(f"no active sheet in {path}")
    return ws


def _set_cell(ws: Worksheet, coord: str, raw: str) -> str:
    """ One validated cell write: dropdown rules enforced, deterministic typing, dates
    inheriting the column's existing format. Returns the change line. """
    _check_validations(ws, coord, raw)
    cell = ws[coord]
    value = _coerce(raw)
    if isinstance(value, datetime) and cell.number_format == "General":
        cell.number_format = _column_date_format(ws, cell.column) or "yyyy-mm-dd"
    change = f"{ws.title}!{coord}: {cell.value!r} -> {value!r}"
    cell.value = value
    return change


def _save_atomic(wb: openpyxl.Workbook, path: Path) -> None:
    tmp = path.with_name(path.name + ".tmp")
    wb.save(tmp)
    os.replace(tmp, path)


def set_cells(assignments: list[str], path: Path = TRACKER_PATH, sheet: str | None = None) -> str:
    """ Apply CELL=VALUE assignments to the tracker in place.

    The low-level write verb: addresses cells directly, for edits the header-keyed
    `add_row`/`update_row` can't express. Same care rules throughout: dropdown rules
    enforced, dates inherit the column's format, formulas refused, atomic save. """

    parsed: list[tuple[str, str]] = []
    for assignment in assignments:
        key, raw = _split_assignment(assignment)
        coord = key.upper()
        if not CELL_REF.fullmatch(coord):
            raise TrackerError(f"expected CELL=VALUE, got {assignment!r}")
        parsed.append((coord, raw))

    wb = _open_for_write(path)
    ws = _sheet(wb, sheet, path)
    changes = [_set_cell(ws, coord, raw) for coord, raw in parsed]
    _save_atomic(wb, path)
    return "\n".join(changes)


def add_row(assignments: list[str], path: Path = TRACKER_PATH, sheet: str | None = None) -> str:
    """ Append a row at the first empty row, from HEADER=VALUE assignments.

    Column-agnostic by construction: headers are read from the sheet at call time, so
    nothing outside the spreadsheet ever needs to know its columns. Values go through
    the same dropdown and typing rules as `set_cells`. """

    pairs = [_split_assignment(a) for a in assignments]
    wb = _open_for_write(path)
    ws = _sheet(wb, sheet, path)
    header_row, headers = _header_row(ws)
    resolved = [(_resolve_header(headers, name), raw) for name, raw in pairs]
    row = _next_row(ws, header_row)
    changes = [_set_cell(ws, f"{letter}{row}", raw) for letter, raw in resolved]
    _save_atomic(wb, path)
    return "\n".join(changes)


def update_row(match: str, assignments: list[str], path: Path = TRACKER_PATH, sheet: str | None = None) -> str:
    """ Update the single row matching `match`, from HEADER=VALUE assignments.

    `match` is a case-insensitive substring tested against every cell. Zero or several
    matching rows refuse loudly, listing the candidates, so a write can never land on a
    row the caller didn't mean. """

    pairs = [_split_assignment(a) for a in assignments]
    wb = _open_for_write(path)
    ws = _sheet(wb, sheet, path)
    header_row, headers = _header_row(ws)
    resolved = [(_resolve_header(headers, name), raw) for name, raw in pairs]

    found = _match_rows(ws, match, header_row)
    if not found:
        raise TrackerError(f"no row matches {match!r}")
    if len(found) > 1:
        listing = "\n".join(f"  row {n}: {preview}" for n, preview in found)
        raise TrackerError(f"{match!r} matches {len(found)} rows; refine it:\n{listing}")

    row, preview = found[0]
    changes = [f"matched row {row}: {preview}"]
    changes += [_set_cell(ws, f"{letter}{row}", raw) for letter, raw in resolved]
    _save_atomic(wb, path)
    return "\n".join(changes)


def describe_tracker(path: Path = TRACKER_PATH) -> str:
    """ Per sheet: column letters, headers, and the rules cells carry (dropdown options,
    date formats). The discovery step that makes `add_row`/`update_row` one-shot — read
    this instead of guessing columns. """

    wb = _load(path)
    blocks: list[str] = []
    for ws in wb.worksheets:
        try:
            _, headers = _header_row(ws)
        except TrackerError:
            blocks.append(f"## {ws.title}\n\n(empty)")
            continue
        dropdowns = _dropdowns(ws)
        lines = [f"## {ws.title}", "", "| Col | Header | Rules |", "| --- | --- | --- |"]
        for display, letter in headers.items():
            rules: list[str] = []
            if letter is None:
                rules.append("duplicate header; address cells with `set`")
            else:
                if letter in dropdowns:
                    rules.append("one of: " + ", ".join(dropdowns[letter]))
                if fmt := _column_date_format(ws, column_index_from_string(letter)):
                    rules.append(f"date ({fmt})")
            lines.append(f"| {letter or '—'} | {_fmt(display)} | {_fmt('; '.join(rules))} |")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)

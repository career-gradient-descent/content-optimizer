""" Deterministic application-tracker access. """

import os
import re
import zipfile
from datetime import date, datetime
from pathlib import Path
from typing import cast

import openpyxl
from openpyxl.utils import get_column_letter
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

    if not path.exists():
        raise TrackerError(f"no tracker at {path} (copy tracker.xlsx.example to {path} to start)")

    try:
        wb = openpyxl.load_workbook(path, data_only=True)
    except InvalidFileException as exc:
        raise TrackerError(f"{path} is not a readable xlsx ({exc})") from exc

    return "\n\n".join(_sheet_markdown(ws, grid=grid) for ws in wb.worksheets)


def _coerce(raw: str) -> object:
    """ Deterministic typing: empty clears, ISO dates become datetimes, numerics become numbers. """
    if raw == "":
        return None
    if ISO_DATE.fullmatch(raw):
        return datetime.strptime(raw, "%Y-%m-%d")
    if re.fullmatch(r"[+-]?[0-9]+", raw):
        return int(raw)
    if re.fullmatch(r"[+-]?[0-9]*\.[0-9]+", raw):
        return float(raw)
    return raw


def _check_validations(ws: Worksheet, coord: str, raw: str) -> None:
    """ Enforce the sheet's own inline list validations (the dropdowns the user
    maintains in Excel/Numbers). Other validation types are left to the apps. """
    validations = cast("list", ws.data_validations.dataValidation)  # openpyxl descriptor confuses ty
    for dv in validations:
        if dv.type != "list" or not dv.formula1 or coord not in dv.sqref:
            continue
        formula = dv.formula1
        if formula.startswith('"') and formula.endswith('"'):
            allowed = formula[1:-1].split(",")
            if raw not in allowed:
                raise TrackerError(
                    f"{coord}: {raw!r} is not in the cell's dropdown {[a for a in allowed if a]}"
                )


def _date_format_for(ws: Worksheet, column: int) -> str:
    """ The column's existing date convention, else ISO. """
    for (cell,) in ws.iter_rows(min_col=column, max_col=column):
        if isinstance(cell.value, (datetime, date)) and cell.number_format != "General":
            return cell.number_format
    return "yyyy-mm-dd"


def set_cells(assignments: list[str], path: Path = TRACKER_PATH, sheet: str | None = None) -> str:
    """ Apply CELL=VALUE assignments to the tracker in place.

    Care rules live here, not in convention: the sheet's own dropdown rules are
    enforced, dates inherit the column's existing format, formulas are refused,
    the load keeps formulas intact (never data_only), and the save is atomic. """

    if not path.exists():
        raise TrackerError(f"no tracker at {path}")

    with zipfile.ZipFile(path) as zf:
        if any(n.startswith(("xl/media/", "xl/charts/", "xl/drawings/")) for n in zf.namelist()):
            raise TrackerError(
                f"{path} contains charts/images, which an openpyxl save silently drops; "
                f"make this edit in Excel/Numbers instead"
            )

    parsed: list[tuple[str, str]] = []
    for assignment in assignments:
        coord, eq, raw = assignment.partition("=")
        coord = coord.strip().upper()
        if not eq or not CELL_REF.fullmatch(coord):
            raise TrackerError(f"expected CELL=VALUE, got {assignment!r}")
        if raw.startswith("="):
            raise TrackerError(f"{coord}: a value starting with '=' would become a formula; refusing")
        parsed.append((coord, raw))

    try:
        wb = openpyxl.load_workbook(path)  # never data_only: formulas must survive the save
    except InvalidFileException as exc:
        raise TrackerError(f"{path} is not a readable xlsx ({exc})") from exc

    if sheet and sheet not in wb.sheetnames:
        raise TrackerError(f"no sheet {sheet!r} in {path} (has: {', '.join(wb.sheetnames)})")
    ws = wb[sheet] if sheet else wb.active
    if ws is None:
        raise TrackerError(f"no active sheet in {path}")

    changes: list[str] = []
    for coord, raw in parsed:
        _check_validations(ws, coord, raw)
        cell = ws[coord]
        value = _coerce(raw)
        if isinstance(value, datetime) and cell.number_format == "General":
            cell.number_format = _date_format_for(ws, cell.column)
        changes.append(f"{ws.title}!{coord}: {cell.value!r} -> {value!r}")
        cell.value = value

    tmp = path.with_name(path.name + ".tmp")
    wb.save(tmp)
    os.replace(tmp, path)
    return "\n".join(changes)

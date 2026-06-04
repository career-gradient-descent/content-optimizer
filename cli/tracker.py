""" Deterministic application-tracker reading. """

from datetime import date, datetime
from pathlib import Path

import openpyxl
from openpyxl.utils.exceptions import InvalidFileException
from openpyxl.worksheet.worksheet import Worksheet

TRACKER_PATH = Path("tracker.xlsx")


class TrackerError(Exception):
    """ Tracker file missing or unreadable. """


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


def _sheet_markdown(ws: Worksheet) -> str:
    rows = [[_fmt(v) for v in row] for row in ws.iter_rows(values_only=True)]
    if not rows:
        return f"## {ws.title}\n\n(empty)"

    header, *body = rows
    width = len(header)

    lines = [
        f"## {ws.title}",
        "",
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(["---"] * width) + " |",
        *("| " + " | ".join(r) + " |" for r in body),
    ]
    return "\n".join(lines)


def read_tracker(path: Path = TRACKER_PATH) -> str:
    """ Dump every sheet of the tracker workbook to faithful markdown.

    Structure-agnostic: assumes nothing about columns, header rows, or sheet count.
    Interpretation is left to the reader. Raises TrackerError when the file is absent. """

    if not path.exists():
        raise TrackerError(f"no tracker at {path} (copy tracker.xlsx.example to {path} to start)")

    try:
        wb = openpyxl.load_workbook(path, data_only=True)
    except InvalidFileException as exc:
        raise TrackerError(f"{path} is not a readable xlsx ({exc})") from exc

    return "\n\n".join(_sheet_markdown(ws) for ws in wb.worksheets)

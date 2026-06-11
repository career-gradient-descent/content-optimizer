""" CLI application. """

from collections.abc import Callable
from pathlib import Path
from typing import Annotated

import typer
import yaml

from cli.core import CompilationError, compile_tex, populate_jinja_template
from cli.fetch import FetchError, fetch_jd_markdown
from cli.schemas.job_description import JobDescriptionSchema
from cli.tracker import (
    TRACKER_PATH,
    TrackerError,
    add_row,
    describe_tracker,
    read_tracker,
    set_cells,
    update_row,
)

app = typer.Typer(
    help="Career content generation toolkit",
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
)

# Major ATS systems identifiable from URL substring.
ATS_URL_PATTERNS = {
    "ashbyhq.com"        : "Ashby",
    "greenhouse.io"      : "Greenhouse",
    "lever.co"           : "Lever",
    "myworkdayjobs.com"  : "Workday",
    "icims.com"          : "iCIMS",
    "smartrecruiters.com": "SmartRecruiters",
    "taleo.net"          : "Taleo",
    "pageuppeople.com"   : "PageUp",
}


def _detect_ats(url: str) -> str:
    return next((name for pattern, name in ATS_URL_PATTERNS.items() if pattern in url), "")


def _emit_frontmatter(fields: dict[str, str]) -> str:
    """ YAML frontmatter where empty values render as `key:` (no `''` clutter). """
    lines = [
        f"{k}:" if not v else yaml.safe_dump({k: v}, default_flow_style=False).rstrip("\n")
        for k, v in fields.items()
    ]
    return "\n".join(lines) + "\n"


@app.command("new-opportunity")
def new_opportunity(
    slug            : Annotated[str, typer.Argument(help="Opportunity slug")],
    role            : Annotated[str, typer.Option(help="Job title")] = "",
    organisation    : Annotated[str, typer.Option(help="Company")] = "",
    location        : Annotated[str, typer.Option(help="Location")] = "",
    url             : Annotated[str, typer.Option(help="Source URL")] = "",
    ats             : Annotated[str, typer.Option(help="ATS system")] = "",
    comp            : Annotated[str, typer.Option(help="Compensation")] = "",
    effort          : Annotated[str, typer.Option(help="Pursuit effort tier")] = "",
) -> None:
    """ Scaffold a new opportunity folder with empty job-description.md. """
    folder: Path = Path("opportunities") / slug
    if folder.exists():
        typer.echo(f"new-opportunity: {folder} already exists", err=True)
        raise typer.Exit(1)
    folder.mkdir(parents=True)
    (folder / "artifacts").mkdir()

    ats = ats or _detect_ats(url)

    jd : JobDescriptionSchema = JobDescriptionSchema(
        role=role, organisation=organisation, location=location,
        url=url, ats=ats, comp=comp, effort=effort,
    )
    frontmatter : str = _emit_frontmatter(jd.model_dump())
    jd_path : Path = folder / "job-description.md"
    jd_path.write_text(f"---\n{frontmatter}---\n\n")
    typer.echo(f"Created: {jd_path}")


@app.command("fetch-jd")
def fetch_jd(
    url: Annotated[str, typer.Argument(help="JD page URL")],
) -> None:
    """ Extract a job description to markdown (deterministic, no LLM). Prints to stdout. """
    try:
        typer.echo(fetch_jd_markdown(url))
    except FetchError as exc:
        typer.echo(f"fetch-jd: {exc}", err=True)
        raise typer.Exit(1)


@app.command()
def render(
    file    : Annotated[Path, typer.Argument(help="YAML or TEX file")],
    template: Annotated[str, typer.Option("-t", help="Template name")] = "primary",
) -> None:
    """ Render PDF. YAML triggers full pipeline; TEX recompiles. """
    if file.suffix == ".tex":
        tex : Path = file
    else:
        tex : Path = file.with_suffix(".tex")
        tex.parent.mkdir(parents=True, exist_ok=True)
        tex.write_text(populate_jinja_template(yaml.safe_load(file.read_text()), file.stem, template))
    try:
        pdf : Path = compile_tex(tex)
    except CompilationError as exc:
        typer.echo(f"render: {exc}", err=True)
        raise typer.Exit(1)
    typer.echo(f"Generated: {pdf}")


tracker_app = typer.Typer(help="Read and edit the application tracker (xlsx).")
app.add_typer(tracker_app, name="tracker")


def _tracker_run(action: Callable[[], str]) -> None:
    """ The one error contract for tracker commands: TrackerError -> one line on stderr, exit 1. """
    try:
        typer.echo(action())
    except TrackerError as exc:
        typer.echo(f"tracker: {exc}", err=True)
        raise typer.Exit(1)


@tracker_app.command("read")
def tracker_read(
    file: Annotated[Path, typer.Argument(help="Tracker xlsx")] = TRACKER_PATH,
    grid: Annotated[bool, typer.Option("--grid", help="Add row numbers + column letters for cell addressing")] = False,
) -> None:
    """ Dump the tracker to markdown. Read-only, deterministic. """
    _tracker_run(lambda: read_tracker(file, grid=grid))


@tracker_app.command("schema")
def tracker_schema(
    file: Annotated[Path, typer.Argument(help="Tracker xlsx")] = TRACKER_PATH,
) -> None:
    """ Describe each sheet: columns, headers, dropdown rules, date formats. Read-only. """
    _tracker_run(lambda: describe_tracker(file))


@tracker_app.command("add")
def tracker_add(
    assignments: Annotated[list[str], typer.Argument(help="HEADER=VALUE ...")],
    sheet      : Annotated[str, typer.Option(help="Sheet name (default: active sheet)")] = "",
    file       : Annotated[Path, typer.Option(help="Tracker xlsx")] = TRACKER_PATH,
) -> None:
    """ Append a row after the last occupied one, keyed by header names. Same rules as set. """
    _tracker_run(lambda: add_row(assignments, path=file, sheet=sheet or None))


@tracker_app.command("update")
def tracker_update(
    assignments: Annotated[list[str], typer.Argument(help="HEADER=VALUE ...")],
    match      : Annotated[str, typer.Option("--match", help="Substring identifying exactly one row")],
    sheet      : Annotated[str, typer.Option(help="Sheet name (default: active sheet)")] = "",
    file       : Annotated[Path, typer.Option(help="Tracker xlsx")] = TRACKER_PATH,
) -> None:
    """ Update the single row matching --match, keyed by header names. Same rules as set. """
    _tracker_run(lambda: update_row(match, assignments, path=file, sheet=sheet or None))


@tracker_app.command("set")
def tracker_set(
    assignments: Annotated[list[str], typer.Argument(help="CELL=VALUE ...")],
    sheet      : Annotated[str, typer.Option(help="Sheet name (default: active sheet)")] = "",
    file       : Annotated[Path, typer.Option(help="Tracker xlsx")] = TRACKER_PATH,
) -> None:
    """ Set cells in place. Dropdown rules enforced; '' clears; dates inherit column format. """
    _tracker_run(lambda: set_cells(assignments, path=file, sheet=sheet or None))


@app.command()
def archive(
    slug: Annotated[str, typer.Argument(help="Opportunity slug")],
) -> None:
    """ Move an opportunity folder into opportunities/.archive/. """
    src : Path = Path("opportunities") / slug
    if not src.is_dir():
        typer.echo(f"archive: no opportunity at {src}", err=True)
        raise typer.Exit(1)

    dest : Path = Path("opportunities") / ".archive" / slug
    if dest.exists():
        typer.echo(f"archive: {dest} already exists", err=True)
        raise typer.Exit(1)

    dest.parent.mkdir(parents=True, exist_ok=True)
    src.rename(dest)
    typer.echo(f"Archived: {src} → {dest}")

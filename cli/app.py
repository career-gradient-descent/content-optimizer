""" CLI application. """

from pathlib import Path
from typing import Annotated

import typer
import yaml

from cli.core import compile_tex, populate_jinja_template
from cli.schemas.job_description import JobDescriptionSchema

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
    """YAML frontmatter where empty values render as `key:` (no `''` clutter)."""
    lines = [
        f"{k}:" if not v else yaml.safe_dump({k: v}, default_flow_style=False).rstrip("\n")
        for k, v in fields.items()
    ]
    return "\n".join(lines) + "\n"


@app.command()
def render(
    file    : Annotated[Path, typer.Argument(help="YAML or TEX file")],
    template: Annotated[str, typer.Option("-t", help="Template name")] = "primary",
) -> None:
    """Render PDF. YAML triggers full pipeline; TEX recompiles."""
    if file.suffix == ".tex":
        tex : Path = file
    else:
        tex : Path = file.with_suffix(".tex")
        tex.parent.mkdir(parents=True, exist_ok=True)
        tex.write_text(populate_jinja_template(yaml.safe_load(file.read_text()), file.stem, template))
    pdf : Path = compile_tex(tex)
    typer.echo(f"Generated: {pdf}")


@app.command("new-opportunity")
def new_opportunity(
    slug            : Annotated[str, typer.Argument(help="Opportunity slug")],
    role            : Annotated[str, typer.Option(help="Job title")] = "",
    organisation    : Annotated[str, typer.Option(help="Company")] = "",
    location        : Annotated[str, typer.Option(help="Location")] = "",
    url             : Annotated[str, typer.Option(help="Source URL")] = "",
    ats             : Annotated[str, typer.Option(help="ATS system")] = "",
    comp            : Annotated[str, typer.Option(help="Compensation")] = "",
) -> None:
    """Scaffold a new opportunity folder with empty job-description.md."""
    folder: Path = Path("opportunities") / slug
    folder.mkdir(parents=True, exist_ok=False)
    (folder / "artifacts").mkdir()

    ats = ats or _detect_ats(url)

    jd : JobDescriptionSchema = JobDescriptionSchema(
        role=role, organisation=organisation, location=location,
        url=url, ats=ats, comp=comp,
    )
    frontmatter : str = _emit_frontmatter(jd.model_dump())
    jd_path : Path = folder / "job-description.md"
    jd_path.write_text(f"---\n{frontmatter}---\n\n")
    typer.echo(f"Created: {jd_path}")

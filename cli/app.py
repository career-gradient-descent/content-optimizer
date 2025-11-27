""" CLI application. """

from pathlib import Path
from typing import Annotated

import typer
import yaml

from cli import OUTPUT_DIR
from cli.core import compile_tex, populate_jinja_template

app         = typer.Typer(help="Career content generation toolkit")
render_app  = typer.Typer(help="Render content from YAML")

app.add_typer(render_app, name="render")


def _render(entity: str, file: Path, template: str, output: Path | None) -> None:
    """ Shared render logic for all entities. """

    pdf: Path = (output or OUTPUT_DIR / f"{file.stem}.pdf").resolve()
    tex: Path = pdf.with_suffix(".tex")
    pdf.parent.mkdir(parents=True, exist_ok=True)

    tex.write_text(
        populate_jinja_template(yaml.safe_load(file.read_text()), entity, template)
    )

    compile_tex(tex)
    typer.echo(f"Generated: {pdf}")


@render_app.command("resume")
def render_resume(
    file    : Annotated[Path, typer.Argument(help="YAML file")],
    template: Annotated[str, typer.Option("-t", help="Template name")] = "primary",
    output  : Annotated[Path | None, typer.Option("-o", help="Output PDF path")] = None,
) -> None:
    """ Render resume PDF from YAML. """
    _render("resume", file, template, output)


@render_app.command("cover-letter")
def render_cover_letter(
    file    : Annotated[Path, typer.Argument(help="YAML file")],
    template: Annotated[str, typer.Option("-t", help="Template name")] = "primary",
    output  : Annotated[Path | None, typer.Option("-o", help="Output PDF path")] = None,
) -> None:
    """ Render cover letter PDF from YAML. """
    _render("cover-letter", file, template, output)


@app.command("re-render")
def re_render(
    file    : Annotated[Path, typer.Argument(help="TEX file")],
    output  : Annotated[Path | None, typer.Option("-o", help="Output PDF path")] = None,
) -> None:
    """ Re-compile TEX to PDF. """
    tex = file.resolve()
    compile_tex(tex)

    src_pdf = tex.with_suffix(".pdf")
    dst_pdf = (output or OUTPUT_DIR / f"{file.stem}.pdf").resolve()

    if src_pdf != dst_pdf:
        dst_pdf.parent.mkdir(parents=True, exist_ok=True)
        src_pdf.rename(dst_pdf)

    typer.echo(f"Generated: {dst_pdf}")

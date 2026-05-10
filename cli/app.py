""" CLI application. """

from pathlib import Path
from typing import Annotated

import typer
import yaml

from cli.core import compile_tex, populate_jinja_template

app = typer.Typer(
    help="Career content generation toolkit",
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
)


@app.command()
def render(
    file    : Annotated[Path, typer.Argument(help="YAML or TEX file")],
    template: Annotated[str, typer.Option("-t", help="Template name")] = "primary",
) -> None:
    """Render PDF. YAML triggers full pipeline; TEX recompiles."""
    if file.suffix != ".tex":
        tex = file.with_suffix(".tex")
        tex.parent.mkdir(parents=True, exist_ok=True)
        tex.write_text(populate_jinja_template(yaml.safe_load(file.read_text()), file.stem, template))
    else:
        tex = file
    compile_tex(tex.resolve())
    typer.echo(f"Generated: {tex.with_suffix('.pdf').resolve()}")


@app.command("new-opportunity")
def new_opportunity(slug: Annotated[str, typer.Argument(help="Opportunity slug")]) -> None:
    """Scaffold a new opportunity folder. (Reserved — implementation pending.)"""
    raise NotImplementedError("Reserved for upcoming opportunity-creation workflow.")

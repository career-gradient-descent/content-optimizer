""" Entity rendering and LaTeX compilation. """

import subprocess
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel as Schema
from pylatex.utils import escape_latex

from cli import TEMPLATE_DIR
from cli.schemas import schemas

LATEX_DOCKER_IMAGE = "texlive/texlive:latest"


def _escape_latex_with_pipe_fix(text: str) -> str:
    """ Escape LaTeX special characters and convert | to $|$ for proper rendering. """
    escaped = escape_latex(text)
    # Replace standalone | with $|$ (LaTeX math mode pipe for proper rendering)
    return escaped.replace("|", "$|$")


def populate_jinja_template(data: dict, entity: str, template: str = "primary") -> str:
    """ Validate data and populate the LaTeX Jinja template for the given entity. """

    schema      : type[Schema]  = schemas[entity]
    validated   : Schema        = schema.model_validate(data)
    template_dir: Path          = TEMPLATE_DIR / entity

    env = Environment(
        loader=FileSystemLoader(template_dir),
        block_start_string="<@",
        block_end_string="@>",
        variable_start_string="<<",
        variable_end_string=">>",
        comment_start_string="<#",
        comment_end_string="#>",
    )
    env.filters["escape_latex"] = _escape_latex_with_pipe_fix

    return env.get_template(f"{template}.tex.j2").render(validated.model_dump())


def compile_tex(tex: Path) -> Path:
    """ Compile LaTeX to PDF via Docker. """

    subprocess.run(
        [
            "docker", "run", "--rm", "-v", f"{tex.parent}:/work", "-w", "/work",
            LATEX_DOCKER_IMAGE, "pdflatex", "-interaction=nonstopmode", tex.name,
        ],
        capture_output=True,
        check=True,
    )

    # Delete auxiliary files
    for ext in (".aux", ".log", ".out"):
        tex.with_suffix(ext).unlink(missing_ok=True)

    return tex.with_suffix(".pdf")

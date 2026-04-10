""" Entity rendering and LaTeX compilation. """

import subprocess
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel as Schema
from pylatex.utils import escape_latex

from cli import TEMPLATE_DIR
from cli.schemas import schemas

LATEX_DOCKER_IMAGE = "texlive/texlive:latest"


class CompilationError(Exception):
    """LaTeX compilation failed."""


def _escape_latex_with_pipe_fix(text: str) -> str:
    """ Escape LaTeX special characters and convert | to $|$ for proper rendering. """
    escaped = escape_latex(text)
    return escaped.replace("|", "$|$")


def populate_jinja_template(data: dict, entity: str, template: str = "primary") -> str:
    """ Validate data and populate the LaTeX Jinja template for the given entity. """

    schema      : type[Schema]  = schemas[entity]
    validated   : Schema        = schema.model_validate(data)
    template_dir: Path          = TEMPLATE_DIR / entity

    env = Environment(
        loader                  =FileSystemLoader(template_dir),
        block_start_string      ="<@",
        block_end_string        ="@>",
        variable_start_string   ="<<",
        variable_end_string     =">>",
        comment_start_string    ="<#",
        comment_end_string      ="#>",
    )
    env.filters["escape_latex"] = _escape_latex_with_pipe_fix

    return env.get_template(f"{template}.tex.j2").render(validated.model_dump())


def _extract_log_errors(log: Path) -> str:
    """Extract error lines from a pdflatex log file."""
    if not log.exists():
        return ""
    lines = []
    for line in log.read_text(errors="replace").splitlines():
        if line.startswith("! ") or line.startswith("l."):
            lines.append(line)
    return "\n".join(lines)


def compile_tex(tex: Path) -> Path:
    """Compile LaTeX to PDF via Docker."""

    pdf = tex.with_suffix(".pdf")

    result = subprocess.run(
        args=[
            "docker", "run", "--rm", "-v", f"{tex.parent}:/work", "-w", "/work",
            LATEX_DOCKER_IMAGE, "pdflatex", "-interaction=nonstopmode", tex.name,
        ],
        capture_output=True,
        text=True,
    )

    log_errors = _extract_log_errors(tex.with_suffix(".log"))

    for ext in (".aux", ".log", ".out"):
        tex.with_suffix(ext).unlink(missing_ok=True)

    if result.returncode != 0:
        raise CompilationError(log_errors or result.stderr or result.stdout or "compilation failed")

    if log_errors:
        print(f"LaTeX warnings:\n{log_errors}", file=sys.stderr)

    if not pdf.exists():
        raise CompilationError("no PDF output produced")

    return pdf

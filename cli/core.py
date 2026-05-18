""" Entity rendering and LaTeX compilation. """

import subprocess
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from pylatex.utils import _latex_special_chars, escape_latex

from cli.schemas import Schema, schemas

# Override pylatex's escape map for prose rendering.
_latex_special_chars |= {
    "~": r"$\sim$",   # prose glyph instead of \textasciitilde{} diacritic
    "|": r"$|$",      # mathmode pipe (pylatex doesn't escape pipes)
    "-": "-",         # pass through (default {-} wrapping kerns oddly)
}

TEMPLATE_DIR = Path(__file__).parent.parent / "templates"

LATEX_DOCKER_IMAGE = "texlive/texlive:latest"

# Custom Jinja delimiters so the templating syntax doesn't conflict with LaTeX's {}.
JINJA_LATEX_DELIMITERS = {
    "block_start_string"    : "<@",
    "block_end_string"      : "@>",
    "variable_start_string" : "<<",
    "variable_end_string"   : ">>",
    "comment_start_string"  : "<#",
    "comment_end_string"    : "#>",
}


class CompilationError(Exception):
    """LaTeX compilation failed."""


def _bold_substring(text: str, substring: str | None) -> str:
    """ Wrap occurrences of `substring` in \\textbf{}. Used to bold the author's own name within an authors list. Both inputs must already be latex-escaped; no escaping is performed here. """
    if not substring:
        return text
    return text.replace(substring, f"\\textbf{{{substring}}}")


def populate_jinja_template(data: dict, entity: str, template: str = "primary") -> str:
    """ Validate data and populate the LaTeX Jinja template for the given entity. """

    schema      : type[Schema]  = schemas[entity]
    validated   : Schema        = schema.model_validate(data)
    template_dir: Path          = TEMPLATE_DIR / entity

    env = Environment(
        loader          =FileSystemLoader(template_dir),
        trim_blocks     =True,
        lstrip_blocks   =True,
        **JINJA_LATEX_DELIMITERS,
    )
    env.filters["escape_latex"] = escape_latex
    env.filters["bold_substring"] = _bold_substring

    return env.get_template(f"{template}.tex.j2").render(validated.model_dump())


def _extract_log_errors(log: Path) -> str:
    """Extract error lines from a pdflatex log file."""
    if not log.exists():
        return ""
    return "\n".join(
        line for line in log.read_text(errors="replace").splitlines()
        if line.startswith(("! ", "l."))
    )


def compile_tex(tex: Path) -> Path:
    """Compile LaTeX to PDF via Docker."""

    tex = tex.resolve()  # docker volume mount requires absolute host path
    pdf = tex.with_suffix(".pdf")

    result = subprocess.run(
        args=[
            "docker", "run", "--rm", "-v", f"{tex.parent}:/work", "-w", "/work",
            LATEX_DOCKER_IMAGE, "pdflatex", "-interaction=nonstopmode", tex.name,
        ],
        capture_output=True,
        text=True,
        check=False
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

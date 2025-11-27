"""Career content generation CLI."""

from pathlib import Path

ROOT            = Path(__file__).parent.parent
TEMPLATE_DIR    = ROOT / "templates"
OUTPUT_DIR      = ROOT / "output"

__all__ = ["TEMPLATE_DIR", "OUTPUT_DIR"]

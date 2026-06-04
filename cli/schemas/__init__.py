""" Schema exports. """

from cli.schemas.base import Schema
from cli.schemas.cover_letter import CoverLetterSchema
from cli.schemas.resume import ResumeSchema

# Renderable entities — those that go through populate_jinja_template → LaTeX → PDF.
# JobDescriptionSchema is intentionally excluded; it's a frontmatter schema, not renderable.
schemas: dict[str, type[Schema]] = {
    "resume"        : ResumeSchema,
    "cover-letter"  : CoverLetterSchema,
}

__all__ = ["Schema", "schemas"]

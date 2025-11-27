""" Schema exports. """

from pydantic import BaseModel as Schema

from cli.schemas.cover_letter import CoverLetterSchema
from cli.schemas.resume import ResumeSchema

schemas: dict[str, type[Schema]] = {
    "resume":       ResumeSchema,
    "cover-letter": CoverLetterSchema,
}

__all__ = ["schemas"]

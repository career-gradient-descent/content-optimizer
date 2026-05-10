""" Schema exports. """

from pydantic import BaseModel, ConfigDict


class Schema(BaseModel):
    """ Shared base. Coerces numbers to strings so unquoted YAML years (e.g. `dates: 2025`)
    validate cleanly against `str` fields without every author having to quote scalars. """

    model_config = ConfigDict(coerce_numbers_to_str=True)


from cli.schemas.cover_letter import CoverLetterSchema
from cli.schemas.resume import ResumeSchema

schemas: dict[str, type[Schema]] = {
    "resume"        : ResumeSchema,
    "cover-letter"  : CoverLetterSchema,
}

__all__ = ["Schema", "schemas"]

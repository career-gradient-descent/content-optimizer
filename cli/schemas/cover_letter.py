""" Cover letter schema (placeholder). """

from pydantic import BaseModel


class CoverLetterSchema(BaseModel):
    """ Placeholder schema - accepts any fields for now. """

    model_config = {"extra": "allow"}

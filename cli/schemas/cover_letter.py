""" Cover letter schema. """

from cli.schemas.base import Schema
from cli.schemas.resume import Link


class CoverLetterSchema(Schema, extra="forbid"):
    """ Cover letter fields consumed by templates/cover-letter/primary.tex.j2. The
    letterhead (name, links) mirrors the resume; body is the one required content field;
    date, recipient, company, subject, and closing are optional. In-body hyperlinks are a
    known limitation: the body renders as escaped LaTeX, so links inside it are added by
    hand-editing the rendered .tex (see cover-letter-strategy.md). """

    name            : str
    links           : list[Link] | None    = None
    date            : str | None            = None
    recipient_name  : str | None            = None
    recipient_title : str | None            = None
    company         : str | None            = None
    subject         : str | None            = None
    body            : str
    closing         : str | None            = None

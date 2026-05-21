""" Resume schema. """

from typing import Literal

from pydantic import Field, field_validator

from cli.schemas import Schema

ATS_KEYWORDS_WORD_LIMIT = 13


class Basics(Schema):
    name            : str
    ats_optimization: str | None = Field(
        None,
        description=r"Invisible ATS keyword text rendered at end of document. Extractable by parsers, not visible to humans. Hard-capped at 13 words.",
    )

    @field_validator("ats_optimization")
    @classmethod
    def _within_word_limit(cls, v: str | None) -> str | None:
        if v and (n := len(v.split())) > ATS_KEYWORDS_WORD_LIMIT:
            raise ValueError(f"ats_optimization must be ≤{ATS_KEYWORDS_WORD_LIMIT} words, got {n}")
        return v


class Link(Schema):
    url     : str
    display : str


class Education(Schema):
    institution     : str
    institution_url : str | None        = None
    degree          : str
    degree_url      : str | None        = None
    dates           : str
    location        : str | None        = None
    details         : list[str] | None  = None


class Experience(Schema):
    company         : str
    company_url     : str | None        = None
    company_tagline : str | None        = Field(
        None,
        description="Rendered after company name, separated by `|`.",
    )
    title           : str
    dates           : str
    location        : str | None        = None
    bullets         : list[str]         = Field(min_length=1)


class Project(Schema):
    name        : str
    url         : str | None        = None
    description : str | None        = None
    tech        : str | None        = Field(
        None,
        description="Rendered after project name in italics, separated by `|`.",
    )
    dates       : str | None        = None
    bullets     : list[str] | None  = None


class Certification(Schema):
    name            : str
    issuer          : str
    date            : str
    credential_id   : str | None = None
    verification_url: str | None = None


class Publication(Schema):
    title       : str
    url         : str | None = None
    authors     : str
    author_self : str | None = None  # substring of `authors` to bold (your own name)
    venue       : str
    year        : str
    status      : Literal["Preprint", "Under review", "Accepted", "In press", "To appear"] | None = None
    note        : str | None = None  # one-line contribution summary


class Meta(Schema):
    subject     : str | None = Field(
        None,
        description=r"PDF metadata `pdfsubject` rendered in \hypersetup{}. Invisible to humans, machine-readable.",
    )
    keywords    : str | None = Field(
        None,
        description=r"PDF metadata `pdfkeywords` rendered in \hypersetup{}. Invisible to humans, machine-readable.",
    )


class ResumeSchema(Schema, extra="forbid"):
    basics          : Basics
    links           : list[Link] | None             = None
    summary         : str | None                    = None
    education       : list[Education]               = Field(min_length=1)
    publications    : list[Publication] | None      = None
    experience      : list[Experience]              = Field(min_length=1)
    projects        : list[Project] | None          = None
    skills          : dict[str, str] | None         = Field(
        None,
        description="Category to comma-separated items. Rendered as labeled lines under Technical Skills.",
    )
    certifications  : list[Certification] | None    = None
    meta            : Meta | None                   = None

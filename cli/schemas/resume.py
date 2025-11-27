""" Resume schema. """

from pydantic import BaseModel, Field


class Basics(BaseModel):
    name            : str
    ats_optimization: str | None = None


class Link(BaseModel):
    url     : str
    display : str


class Education(BaseModel):
    institution : str
    degree      : str
    dates       : str
    location    : str | None        = None
    details     : list[str] | None  = None


class Experience(BaseModel):
    company     : str
    title       : str
    dates       : str
    location    : str | None    = None
    bullets     : list[str]     = Field(min_length=1)


class Project(BaseModel):
    name        : str
    description : str | None        = None
    tech        : str | None        = None
    dates       : str | None        = None
    link        : str | None        = None
    bullets     : list[str] | None  = None


class Certification(BaseModel):
    name            : str
    issuer          : str
    date            : str
    credential_id   : str | None = None
    verification_url: str | None = None


class Meta(BaseModel):
    subject     : str | None = None
    keywords    : str | None = None


class ResumeSchema(BaseModel, extra="forbid"):
    basics          : Basics
    links           : list[Link] | None             = None
    summary         : str | None                    = None
    education       : list[Education]               = Field(min_length=1)
    experience      : list[Experience]              = Field(min_length=1)
    projects        : list[Project] | None          = None
    skills          : dict[str, str] | None         = None
    certifications  : list[Certification] | None    = None
    meta            : Meta | None                   = None

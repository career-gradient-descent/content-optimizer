""" Job description frontmatter schema. """

from cli.schemas.base import Schema


class JobDescriptionSchema(Schema):
    role         : str = ""
    organisation : str = ""
    location     : str = ""
    url          : str = ""
    ats          : str = ""
    comp         : str = ""

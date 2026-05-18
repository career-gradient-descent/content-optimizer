""" Job description frontmatter schema. """

from cli.schemas import Schema


class JobDescriptionSchema(Schema):
    role         : str = ""
    organisation : str = ""
    location     : str = ""
    url          : str = ""
    ats          : str = ""
    comp         : str = ""

""" Shared schema base. """

from pydantic import BaseModel, ConfigDict


class Schema(BaseModel):
    """ Shared base. Coerces numbers to strings so unquoted YAML years (e.g. `dates: 2025`)
    validate cleanly against `str` fields without every author having to quote scalars. """

    model_config = ConfigDict(coerce_numbers_to_str=True, extra="forbid")

from typing import Any, Callable

from src.unclaimed_property.models.property_record import PropertyRecord
from src.unclaimed_property.parsers.texas import parse_response as parse_texas_response
from src.unclaimed_property.parsers.new_york import parse_response as parse_new_york_response
from src.unclaimed_property.parsers.california import parse_response as parse_california_response
from src.unclaimed_property.parsers.florida import parse_response as parse_florida_response
from src.unclaimed_property.parsers.pennsylvania import parse_response as parse_pennsylvania_response
from src.unclaimed_property.parsers.vermont import parse_response as parse_vermont_response
from src.unclaimed_property.parsers.wisconsin import parse_response as parse_wisconsin_response
from src.unclaimed_property.parsers.missouri import parse_response as parse_missouri_response
from src.unclaimed_property.parsers.alaska import parse_response as parse_alaska_response
from src.unclaimed_property.parsers.alabama import parse_response as parse_alabama_response
from src.unclaimed_property.parsers.arkansas import parse_response as parse_arkansas_response
from src.unclaimed_property.parsers.arizona import parse_response as parse_arizona_response


ParserFunction = Callable[[dict[str, Any]], list[PropertyRecord]]


PARSERS = {
    "TX": parse_texas_response,
    "NY": parse_new_york_response,
    "CA": parse_california_response,
    "FL": parse_florida_response,
    "PA": parse_pennsylvania_response,
    "VT": parse_vermont_response,
    "WI": parse_wisconsin_response,
    "MO": parse_missouri_response,
    "AK": parse_alaska_response,
    "AL": parse_alabama_response,
    "AR": parse_arkansas_response,
    "AZ": parse_arizona_response
}


def get_parser(state_code: str) -> ParserFunction:
    normalized_state = state_code.upper().strip()

    if normalized_state not in PARSERS:
        available = ", ".join(sorted(PARSERS.keys()))
        raise ValueError(
            f"No parser registered for state '{state_code}'. "
            f"Available parsers: {available}"
        )

    return PARSERS[normalized_state]
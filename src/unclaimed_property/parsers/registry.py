from typing import Any, Callable

from src.unclaimed_property.models.property_record import PropertyRecord
from src.unclaimed_property.parsers.sws import build_sws_parser
from src.unclaimed_property.parsers.florida import parse_response as parse_florida_response
from src.unclaimed_property.parsers.georgia import parse_response as parse_georgia_response


ParserFunction = Callable[[dict[str, Any]], list[PropertyRecord]]


SWS_STATES = [
    "AK", "AL", "AR", "AZ",
    "CA", "CO", "CT", "DE",
    "HI",
    "IA", "ID", "IL", "IN",
    "KS", "KY",
    "LA",
    "MA", "MD", "ME", "MI", "MN", "MO", "MS", "MT",
    "NC", "ND", "NE", "NH", "NJ", "NM", "NV",
    "NY",
    "OH", "OK", "OR",
    "PA",
    "RI",
    "SC", "SD", "TN", "TX",
    "UT", "VA", "VT", "WA", "WI", "WV", "WY",
]


PARSERS: dict[str, ParserFunction] = {
    "FL": parse_florida_response,
    "GA": parse_georgia_response,
}


for state in SWS_STATES:
    PARSERS[state] = build_sws_parser(state)


def get_parser(state_code: str) -> ParserFunction:
    normalized_state = state_code.upper().strip()

    if normalized_state not in PARSERS:
        available = ", ".join(sorted(PARSERS.keys()))
        raise ValueError(
            f"No parser registered for state '{state_code}'. "
            f"Available parsers: {available}"
        )

    return PARSERS[normalized_state]
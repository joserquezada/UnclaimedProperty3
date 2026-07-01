from typing import Any, Callable

from src.unclaimed_property.models.property_record import PropertyRecord
from src.unclaimed_property.parsers.texas import parse_response as parse_texas_response


ParserFunction = Callable[[dict[str, Any]], list[PropertyRecord]]


PARSERS: dict[str, ParserFunction] = {
    "TX": parse_texas_response,
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
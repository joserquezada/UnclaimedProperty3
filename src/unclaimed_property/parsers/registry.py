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
from src.unclaimed_property.parsers.colorado import parse_response as parse_colorado_response
from src.unclaimed_property.parsers.connecticut import parse_response as parse_connecticut_response
from src.unclaimed_property.parsers.delaware import parse_response as parse_delaware_response
from src.unclaimed_property.parsers.iowa import parse_response as parse_iowa_response
from src.unclaimed_property.parsers.idaho import parse_response as parse_idaho_response
from src.unclaimed_property.parsers.indiana import parse_response as parse_indiana_response
from src.unclaimed_property.parsers.illinois import parse_response as parse_illinois_response
from src.unclaimed_property.parsers.georgia import parse_response as parse_georgia_response
from src.unclaimed_property.parsers.kansas import parse_response as parse_kansas_response
from src.unclaimed_property.parsers.louisiana import parse_response as parse_louisiana_response
from src.unclaimed_property.parsers.maine import parse_response as parse_maine_response
from src.unclaimed_property.parsers.maryland import parse_response as parse_maryland_response
from src.unclaimed_property.parsers.massachusetts import parse_response as parse_massachusetts_response
from src.unclaimed_property.parsers.michigan import parse_response as parse_michigan_response
from src.unclaimed_property.parsers.minnesota import parse_response as parse_minnesota_response
from src.unclaimed_property.parsers.mississippi import parse_response as parse_mississippi_response



ParserFunction = Callable[[dict[str, Any]], list[PropertyRecord]]


PARSERS = {
    "AL": parse_alabama_response,
    "AK": parse_alaska_response,
    "AZ": parse_arizona_response,
    "AR": parse_arkansas_response,
    "CA": parse_california_response,
    "CO": parse_colorado_response,
    "CT": parse_connecticut_response,
    "DE": parse_delaware_response,
    "FL": parse_florida_response,
    "GA": parse_georgia_response,
    "HI": parse_hawaii_response,
    "ID": parse_idaho_response,
    "IL": parse_illinois_response,
    "IN": parse_indiana_response,
    "IA": parse_iowa_response,
    "KS": parse_kansas_response,
    "KY": parse_kentucky_response,
    "LA": parse_louisiana_response,
    "ME": parse_maine_response,
    "MD": parse_maryland_response,
    "MA": parse_massachusetts_response,
    "MI": parse_michigan_response,
    "MN": parse_minnesota_response,
    "MS": parse_mississippi_response,
    "MO": parse_missouri_response,
    "MT": parse_montana_response,
    "NE": parse_nebraska_response,
    "NV": parse_nevada_response,
    "NH": parse_new_hampshire_response,
    "NJ": parse_new_jersey_response,
    "NM": parse_new_mexico_response,
    "NY": parse_new_york_response,
    "NC": parse_north_carolina_response,
    "ND": parse_north_dakota_response,
    "OH": parse_ohio_response,
    "OK": parse_oklahoma_response,
    "OR": parse_oregon_response,
    "PA": parse_pennsylvania_response,
    "RI": parse_rhode_island_response,
    "SC": parse_south_carolina_response,
    "SD": parse_south_dakota_response,
    "TN": parse_tennessee_response,
    "TX": parse_texas_response,
    "UT": parse_utah_response,
    "VT": parse_vermont_response,
    "VA": parse_virginia_response,
    "WA": parse_washington_response,
    "WV": parse_west_virginia_response,
    "WI": parse_wisconsin_response,
    "WY": parse_wyoming_response,
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
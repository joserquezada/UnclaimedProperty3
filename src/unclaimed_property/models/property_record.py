from dataclasses import dataclass


@dataclass(slots=True)
class PropertyRecord:
    source_state: str
    property_id: int
    owner_name: str
    holder_name: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    property_type: str | None = None
    property_type_code: str | None = None
    property_value: float | None = None
    property_value_description: str | None = None
    report_year: str | None = None
    uuid: str | None = None
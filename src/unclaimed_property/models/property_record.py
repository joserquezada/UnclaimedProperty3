from dataclasses import dataclass


@dataclass(slots=True)
class PropertyRecord:
    source_state: str

    property_id: int

    owner_name: str

    holder_name: str

    address: str

    city: str

    state: str

    postal_code: str

    property_type: str

    property_type_code: str

    property_value: float | None
    
    property_value_description: str | None

    report_year: str

    uuid: str
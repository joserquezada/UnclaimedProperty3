from typing import Any

from src.unclaimed_property.models.property_record import PropertyRecord

def parse_property_value(record: dict) -> float | None:
    value = record.get("propertyValue")

    if isinstance(value, (int, float)):
        return float(value)

    text = record.get("propertyValueDescription")

    if not text:
        return None

    clean = str(text).replace("$", "").replace(",", "").strip()

    try:
        return float(clean)
    except ValueError:
        return None

def build_sws_parser(source_state: str):
    def parse_property(record: dict[str, Any]) -> PropertyRecord:
        owner_name = record.get("ownerName", "")
        second_owner = (record.get("secondOwnerName") or "").strip()

        if second_owner:
            owner_name = f"{owner_name} / {second_owner}"

        return PropertyRecord(
            source_state=source_state,
            property_id=record.get("propertyID"),
            owner_name=owner_name,
            holder_name=record.get("holderName"),
            address=record.get("address1"),
            city=record.get("city"),
            state=record.get("state") or source_state,
            postal_code=record.get("postalCode"),
            property_type=record.get("propertyTypeDescription"),
            property_type_code=record.get("propertyTypeCD"),
            property_value=parse_property_value(record),
            report_year=record.get("reportYear"),
            uuid=record.get("uuid"),
        )

    def parse_response(data: dict[str, Any]) -> list[PropertyRecord]:
        return [parse_property(record) for record in data.get("properties", [])]

    return parse_response
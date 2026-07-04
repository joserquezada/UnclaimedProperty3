from typing import Any

from src.unclaimed_property.models.property_record import PropertyRecord


def parse_property(record: dict[str, Any]) -> PropertyRecord:
    return PropertyRecord(
        source_state="MO",
        property_id=record.get("propertyID"),
        owner_name=record.get("ownerName"),
        holder_name=record.get("holderName"),
        address=record.get("address1"),
        city=record.get("city"),
        state=record.get("state"),
        postal_code=record.get("postalCode"),
        property_type=record.get("propertyTypeDescription"),
        property_type_code=record.get("propertyTypeCD"),
        property_value=record.get("propertyValue"),
        report_year=record.get("reportYear"),
        uuid=record.get("uuid"),
    )


def parse_response(data: dict[str, Any]) -> list[PropertyRecord]:
    properties = data.get("properties", [])
    return [parse_property(record) for record in properties]
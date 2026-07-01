from typing import Any

from src.unclaimed_property.models.property_record import PropertyRecord


def parse_property(record: dict[str, Any]) -> PropertyRecord:
    owner_name = record.get("ownerName", "")
    second_owner = record.get("secondOwnerName", "")

    if second_owner.strip():
        owner_name = f"{owner_name} / {second_owner}"
    property_value_text = record.get("propertyValueDescription")

    if property_value_text:
        try:
            property_value = float(
                property_value_text.replace("$", "").replace(",", "")
            )
        except ValueError:
            property_value = None
    else:
        property_value = None
        

    return PropertyRecord(
        source_state="CA",
        property_id=record.get("propertyID"),
        owner_name=owner_name,
        holder_name=record.get("holderName"),
        address=record.get("address1"),
        city=record.get("city"),
        state=record.get("state"),
        postal_code=record.get("postalCode"),
        property_type=record.get("propertyTypeDescription"),
        property_type_code=record.get("propertyTypeCD"),
        property_value=property_value,
        report_year=record.get("reportYear"),
        uuid=record.get("uuid"),
    )

def parse_response(data: dict[str, Any]) -> list[PropertyRecord]:
    properties = data.get("properties", [])
    return [parse_property(record) for record in properties]
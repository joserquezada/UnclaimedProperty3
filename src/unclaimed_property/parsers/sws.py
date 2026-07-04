from typing import Any

from src.unclaimed_property.models.property_record import PropertyRecord


def parse_value_fields(record: dict[str, Any]) -> tuple[float | None, str | None]:
    raw_value = record.get("propertyValue")
    value_description = record.get("propertyValueDescription")

    if isinstance(raw_value, (int, float)):
        return float(raw_value), value_description

    if not value_description:
        return None, None

    clean = str(value_description).replace("$", "").replace(",", "").strip()

    try:
        return float(clean), str(value_description)
    except ValueError:
        return None, str(value_description)


def build_sws_parser(source_state: str):
    def parse_property(record: dict[str, Any]) -> PropertyRecord:
        owner_name = record.get("ownerName", "")
        second_owner = (record.get("secondOwnerName") or "").strip()

        if second_owner:
            owner_name = f"{owner_name} / {second_owner}"

        property_value, property_value_description = parse_value_fields(record)

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
            property_value=property_value,
            property_value_description=property_value_description,
            report_year=record.get("reportYear"),
            uuid=record.get("uuid"),
        )

    def parse_response(data: dict[str, Any]) -> list[PropertyRecord]:
        return [parse_property(record) for record in data.get("properties", [])]

    return parse_response
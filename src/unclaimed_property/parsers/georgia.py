from typing import Any

from src.unclaimed_property.models.property_record import PropertyRecord


def parse_property(record: dict[str, Any]) -> PropertyRecord:
    return PropertyRecord(
        source_state="GA",
        property_id=record.get("PropId"),
        owner_name=record.get("PrtyNm"),
        holder_name=None,
        address=None,
        city=record.get("CityNm"),
        state=record.get("StCd") or "GA",
        postal_code=record.get("ZoneUsaPstlCd"),
        property_type=None,
        property_type_code=None,
        property_value=None,
        property_value_description=record.get("PropAmt"),
        report_year=None,
        uuid=None,
    )


def parse_response(data: dict[str, Any]) -> list[PropertyRecord]:
    properties = data.get("properties", [])
    return [parse_property(record) for record in properties]
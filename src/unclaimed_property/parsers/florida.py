from typing import Any

from src.unclaimed_property.models.property_record import PropertyRecord


def parse_property(record: dict[str, Any]) -> PropertyRecord:
    return PropertyRecord(
        source_state="FL",
        property_id=record.get("PropId"),
        owner_name=record.get("ReportedOwner"),
        holder_name=record.get("PrtyRptNm"),
        address=record.get("AddrDsc"),
        city=record.get("CityNm"),
        state=record.get("StCd"),
        postal_code=record.get("ZoneUsaPstlCd"),
        property_type=record.get("PrclTypeDsc"),
        property_type_code=record.get("PrclCd"),
        property_value=record.get("PropAmt"),
        report_year=None,
        uuid=None,
    )


def parse_response(data: dict[str, Any]) -> list[PropertyRecord]:
    properties = data.get("properties", [])
    return [parse_property(record) for record in properties]
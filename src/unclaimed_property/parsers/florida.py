from typing import Any

from src.unclaimed_property.models.property_record import PropertyRecord


def parse_property(record: dict[str, Any]) -> PropertyRecord:
    return PropertyRecord(
        source_state="FL",
        property_id=record.get("PropId"),
        owner_name=record.get("ReportedOwner") or record.get("PrtyNm"),
        holder_name=record.get("PrtyRptNm"),
        address=record.get("AddrDsc"),
        city=record.get("CityNm"),
        state=record.get("StCd") or "FL",
        postal_code=record.get("ZoneUsaPstlCd"),
        property_type=record.get("PrclTypeDsc"),
        property_type_code=record.get("PrclCd") or record.get("StatCd"),
        property_value=record.get("PropAmt"),
        property_value_description=None,
        report_year=None,
        uuid=None,
    )


def parse_response(data: dict[str, Any]) -> list[PropertyRecord]:
    return [parse_property(record) for record in data.get("properties", [])]
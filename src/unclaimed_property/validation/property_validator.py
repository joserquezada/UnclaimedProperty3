from src.unclaimed_property.models.property_record import PropertyRecord


def validate_record(record: PropertyRecord) -> list[str]:
    errors = []

    if record.property_id is None:
        errors.append("Missing property_id")

    if not record.owner_name or record.owner_name.strip() == "":
        errors.append("Missing owner_name")

    if record.property_value is None:
        errors.append("Missing property_value")

    if not record.source_state or record.source_state.strip() == "":
        errors.append("Missing source_state")

    return errors
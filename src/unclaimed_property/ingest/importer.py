import json
import sys
from pathlib import Path

from src.unclaimed_property.parsers.registry import get_parser
from src.unclaimed_property.export.csv_exporter import write_records_to_csv
from src.unclaimed_property.validation.property_validator import validate_record
from src.unclaimed_property.database.duckdb_repository import DuckDBRepository


def load_json_file(file_path: Path) -> dict:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def main() -> None:
    if len(sys.argv) != 4:
        print("Usage: python -m src.unclaimed_property.ingest.importer <state> <input-json> <output-csv>")
        sys.exit(1)

    state_code = sys.argv[1]
    input_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3])

    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    data = load_json_file(input_path)
    parser = get_parser(state_code)
    records = parser(data)

    invalid_count = 0
    for record in records:
        errors = validate_record(record)
        if errors:
            invalid_count += 1

    print("Parsed records:", len(records))
    print("Invalid records:", invalid_count)
    write_records_to_csv(records, output_path)
    repo = DuckDBRepository(Path("data/database/unclaimed_property.duckdb"))
    repo.initialize()
    repo.save_properties(records)
    print()

    print("DuckDB Verification")
    print("-------------------")

    print("Property Count:", repo.count_properties())

    print()

    print(repo.get_first_property())
    
    print()
    
    


if __name__ == "__main__":
    main()
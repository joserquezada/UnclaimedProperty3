import json
import sys
from pathlib import Path

from src.unclaimed_property.parsers.texas import parse_response
from src.unclaimed_property.export.csv_exporter import write_records_to_csv


def load_json_file(file_path: Path) -> dict:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python -m src.unclaimed_property.ingest.importer <input-json> <output-csv>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    data = load_json_file(input_path)
    records = parse_response(data)

    print("Parsed records:", len(records))

    write_records_to_csv(records, output_path)


if __name__ == "__main__":
    main()
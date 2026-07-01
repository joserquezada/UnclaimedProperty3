import json
import sys
from pathlib import Path

from src.unclaimed_property.parsers.texas import parse_response


def load_json_file(file_path: Path) -> dict:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python python/ingest/importer.py <path-to-json>")
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(f"File not found: {file_path}")
        sys.exit(1)

    data = load_json_file(file_path)
    records = parse_response(data)

    print("Parsed records:", len(records))
    print(records[0])


if __name__ == "__main__":
    main()
import csv
import json
import sys
from dataclasses import asdict
from pathlib import Path

from src.unclaimed_property.parsers.registry import get_parser


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python -m src.unclaimed_property.cli.export_state <STATE> <RAW_STATE_FOLDER>")
        sys.exit(1)

    state_code = sys.argv[1].upper().strip()
    raw_folder = Path(sys.argv[2])

    parser = get_parser(state_code)

    json_files = sorted(raw_folder.glob("*.json"))

    if not json_files:
        print(f"{state_code}: No JSON files found. Skipping.")
        return

    all_records = []

    for json_path in json_files:
        if not json_path.is_file():
            continue

        with json_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        records = parser(data)
        all_records.extend(records)

        print(f"{json_path.name}: {len(records)} records")

    if not all_records:
        print("No records found.")
        return

    output_folder = Path("data/processed") / state_code
    output_folder.mkdir(parents=True, exist_ok=True)

    output_path = output_folder / "combined.csv"

    fieldnames = list(asdict(all_records[0]).keys())

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for record in all_records:
            writer.writerow(asdict(record))

    print()
    print(f"Combined records: {len(all_records)}")
    print(f"CSV written to: {output_path}")


if __name__ == "__main__":
    main()
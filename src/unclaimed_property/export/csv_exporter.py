import csv
from pathlib import Path
from typing import Any
from dataclasses import asdict


def write_records_to_csv(records: list[dict[str, Any]], output_path: Path) -> None:
    if not records:
        print("No records to export.")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(asdict(records[0]).keys())

    with open(output_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(asdict(record) for record in records)

    print(f"CSV written to: {output_path}")
import json
from pathlib import Path

from src.unclaimed_property.database.duckdb_repository import DuckDBRepository
from src.unclaimed_property.parsers.registry import get_parser


RAW_ROOT = Path("data/raw")
DATABASE_PATH = Path("data/database/unclaimed_property.duckdb")


def main() -> None:
    repo = DuckDBRepository(DATABASE_PATH)
    repo.initialize()

    total_states = 0
    total_files = 0
    total_parsed = 0
    total_inserted = 0

    print()
    print("=" * 50)
    print("Building Nationwide Database")
    print("=" * 50)

    for state_folder in sorted(RAW_ROOT.iterdir()):
        if not state_folder.is_dir():
            continue

        state_code = state_folder.name.upper()
        json_files = sorted(state_folder.glob("*.json"))

        if not json_files:
            print(f"{state_code}: No JSON files found. Skipping.")
            continue

        parser = get_parser(state_code)

        state_parsed = 0
        state_inserted = 0

        print()
        print(f"{state_code}")
        print("-" * 50)

        for json_path in json_files:
            with json_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            records = parser(data)
            inserted = repo.save_properties(records)

            file_parsed = len(records)

            state_parsed += file_parsed
            state_inserted += inserted
            total_files += 1

            print(f"{json_path.name}: parsed {file_parsed}, inserted {inserted}")

        total_states += 1
        total_parsed += state_parsed
        total_inserted += state_inserted

        print(f"{state_code} total: parsed {state_parsed}, inserted {state_inserted}")

    print()
    print("=" * 50)
    print("Build Summary")
    print("=" * 50)
    print(f"States processed: {total_states}")
    print(f"JSON files processed: {total_files}")
    print(f"Records parsed: {total_parsed}")
    print(f"Records inserted: {total_inserted}")
    print(f"Database total: {repo.count_properties()}")


if __name__ == "__main__":
    main()
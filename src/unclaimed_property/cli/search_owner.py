import sys
from pathlib import Path

from src.unclaimed_property.database.duckdb_repository import DuckDBRepository


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m src.unclaimed_property.cli.search_owner <owner-name>")
        sys.exit(1)

    owner_query = sys.argv[1]

    repo = DuckDBRepository(Path("data/database/unclaimed_property.duckdb"))

    results = repo.search_owner_totals(owner_query)

    print()
    print(f"Owner Search: {owner_query}")
    print("-" * 40)

    if not results:
        print("No matching records found.")
        return

    for source_state, owner_name, property_count, total_value in results:
        print(
            f"{source_state} | {owner_name} | "
            f"{property_count} properties | ${total_value:,.2f}"
        )


if __name__ == "__main__":
    main()
from dataclasses import asdict
from pathlib import Path

import duckdb

from src.unclaimed_property.models.property_record import PropertyRecord


class DuckDBRepository:
    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)

    def initialize(self) -> None:
        with duckdb.connect(str(self.database_path)) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS properties (
                    source_state VARCHAR,
                    property_id BIGINT,
                    owner_name VARCHAR,
                    holder_name VARCHAR,
                    address VARCHAR,
                    city VARCHAR,
                    state VARCHAR,
                    postal_code VARCHAR,
                    property_type VARCHAR,
                    property_type_code VARCHAR,
                    property_value DOUBLE,
                    report_year VARCHAR,
                    uuid VARCHAR
                )
                """
            )

    def save_properties(self, records: list[PropertyRecord]) -> None:
        if not records:
            print("No records to save.")
            return

        rows = [
            tuple(asdict(record).values())
            for record in records
        ]

        with duckdb.connect(str(self.database_path)) as conn:
            conn.executemany(
                """
                INSERT INTO properties (
                    source_state,
                    property_id,
                    owner_name,
                    holder_name,
                    address,
                    city,
                    state,
                    postal_code,
                    property_type,
                    property_type_code,
                    property_value,
                    report_year,
                    uuid
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                rows,
            )

        print(f"Saved {len(records)} records to DuckDB.")
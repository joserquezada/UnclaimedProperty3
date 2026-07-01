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

        inserted_count = 0

        with duckdb.connect(str(self.database_path)) as conn:
            for record in records:
                values = tuple(asdict(record).values())

                exists = conn.execute(
                    """
                    SELECT COUNT(*)
                    FROM properties
                    WHERE source_state = ?
                    AND property_id = ?
                    AND owner_name = ?
                    AND holder_name = ?
                    AND address = ?
                    AND city = ?
                    AND state = ?
                    AND postal_code = ?
                    AND property_type = ?
                    AND property_type_code = ?
                    AND property_value = ?
                    AND report_year = ?
                    AND uuid = ?
                    """,
                    values,
                ).fetchone()[0]

                if exists == 0:
                    conn.execute(
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
                        values,
                    )
                    inserted_count += 1

        print(f"Inserted {inserted_count} new records into DuckDB.")

    def count_properties(self) -> int:
        with duckdb.connect(str(self.database_path)) as conn:
            result = conn.execute(
                """
                SELECT COUNT(*)
                FROM properties
                """
            ).fetchone()

        return result[0]
    
    def get_first_property(self):
        with duckdb.connect(str(self.database_path)) as conn:
            return conn.execute(
                """
                SELECT *
                FROM properties
                LIMIT 1
                """
            ).fetchone()
            
    def search_owner_totals(self, owner_query: str):
        pattern = f"%{owner_query.upper()}%"

        with duckdb.connect(str(self.database_path)) as conn:
            return conn.execute(
                """
                SELECT
                    source_state,
                    owner_name,
                    address,
                    city,
                    state,
                    postal_code,
                    COUNT(*) AS property_count,
                    SUM(property_value) AS total_value
                FROM properties
                WHERE UPPER(owner_name) LIKE ?
                GROUP BY
                    source_state,
                    owner_name,
                    address,
                    city,
                    state,
                    postal_code
                ORDER BY total_value DESC
                """,
                [pattern],
            ).fetchall()
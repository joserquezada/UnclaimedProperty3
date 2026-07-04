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
                    property_value_description VARCHAR,
                    report_year VARCHAR,
                    uuid VARCHAR
                )
                """
            )

            conn.execute(
                """
                ALTER TABLE properties
                ADD COLUMN IF NOT EXISTS property_value_description VARCHAR
                """
            )

    def save_properties(self, records: list[PropertyRecord]) -> None:
        if not records:
            print("No records to save.")
            return

        inserted_count = 0

        with duckdb.connect(str(self.database_path)) as conn:
            for record in records:
                values = (
                    record.source_state,
                    record.property_id,
                    record.owner_name,
                    record.holder_name,
                    record.address,
                    record.city,
                    record.state,
                    record.postal_code,
                    record.property_type,
                    record.property_type_code,
                    record.property_value,
                    record.property_value_description,
                    record.report_year,
                    record.uuid,
                )

                exists = conn.execute(
                    """
                    SELECT COUNT(*)
                    FROM properties
                    WHERE source_state IS NOT DISTINCT FROM ?
                    AND property_id IS NOT DISTINCT FROM ?
                    AND owner_name IS NOT DISTINCT FROM ?
                    AND holder_name IS NOT DISTINCT FROM ?
                    AND address IS NOT DISTINCT FROM ?
                    AND city IS NOT DISTINCT FROM ?
                    AND state IS NOT DISTINCT FROM ?
                    AND postal_code IS NOT DISTINCT FROM ?
                    AND property_type IS NOT DISTINCT FROM ?
                    AND property_type_code IS NOT DISTINCT FROM ?
                    AND property_value IS NOT DISTINCT FROM ?
                    AND property_value_description IS NOT DISTINCT FROM ?
                    AND report_year IS NOT DISTINCT FROM ?
                    AND uuid IS NOT DISTINCT FROM ?
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
                            property_value_description,
                            report_year,
                            uuid
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                    SUM(property_value) AS total_value,
                    COUNT(*) FILTER (WHERE property_value IS NULL AND property_value_description IS NOT NULL) AS described_value_count,
                    COUNT(*) FILTER (WHERE property_value IS NULL AND property_value_description IS NULL) AS unknown_value_count
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
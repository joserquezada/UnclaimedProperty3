import json
import sys
from pathlib import Path


def inspect_json(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("=" * 50)
    print("JSON INSPECTION")
    print("=" * 50)

    print("\nTop-Level Keys")
    print("-" * 20)

    for key in data.keys():
        print(key)

    properties = data.get("properties", [])

    print("\nNumber of Properties")
    print("-" * 20)
    print(len(properties))

    if properties:
        print("\nProperty Fields")
        print("-" * 20)

        for field in properties[0].keys():
            print(field)

        print("\nField Types")
        print("-" * 20)

        field_types = {}
        
        for record in properties:
            for field, value in record.items():
                field_types.setdefault(field, set())
                field_types[field].add(type(value).__name__)

        for field, types in field_types.items():
            print(f"{field}: {sorted(types)}")
            
        print("\nMissing / Blank Values")
        print("-" * 20)

        for field in field_types.keys():
            missing_count = 0

            for record in properties:
                value = record.get(field)

                if value is None:
                    missing_count += 1
                elif isinstance(value, str) and value.strip() == "":
                    missing_count += 1

            print(f"{field}: {missing_count}")
    
    expected_fields = set(properties[0].keys())
    for index, record in enumerate(properties):
        if set(record.keys()) != expected_fields:
            print(f"Record {index} has a different schema.")


def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("python python/inspect_json.py <json file>")
        return

    inspect_json(Path(sys.argv[1]))


if __name__ == "__main__":
    main()
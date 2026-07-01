import json
from pathlib import Path

json_file = Path("../data/raw/texas_response.json")

with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

print(type(data))
print(data.keys())
print(len(data["properties"]))
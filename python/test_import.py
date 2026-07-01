import json
from pathlib import Path

json_file = Path("../data/raw/texas_response.json")

with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

print(type(data))
print(data.keys())
print(len(data["properties"]))
print(data["searchResults"])
print(data["anyExactMatch"])
print(data["score"])
first = data["properties"][0]

print(first.keys())
first = data["properties"][0]

for key, value in first.items():
    print(f"{key}: {value} ({type(value).__name__})")
    
properties = data["properties"]

print("\nSUMMARY")
print("Total properties:", len(properties))
print("Exact match:", data["anyExactMatch"])
print("First owner:", properties[0]["ownerName"])
print("First holder:", properties[0]["holderName"])
print("First value:", properties[0]["propertyValue"])
print("First city:", properties[0]["city"])
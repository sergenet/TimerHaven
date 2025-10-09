import json

with open("world-cities.json") as f:
    zones = json.load(f)

cities = []
for zone in zones:
    for tz in zone.get("utc", []):
        # Use the last part as city name, or customize mapping if needed
        if "/" in tz:
            name = tz.split("/")[-1].replace("_", " ")
            cities.append({"name": name, "timezone": tz})

with open("cities-converted.json", "w") as f:
    json.dump(cities, f, indent=2)
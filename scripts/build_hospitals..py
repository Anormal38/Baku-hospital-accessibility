import requests
import csv
import re

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

BLACKLIST = [
    "dental", "stomatolo", "eye", "göz", "oftalm",
    "plastic", "estetik", "vet", "dermatolo",
    "poliklinika", "clinic"
]


def safe_filename(name: str) -> str:

    name = name.lower()
    name = re.sub(r"[^\w\-]", "_", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_")


def is_emergency_capable(tags: dict) -> bool:

    if tags.get("amenity") != "hospital":
        return False

    if tags.get("emergency") == "yes":
        return True

    if tags.get("hospital:type") in ["general", "district", "regional"]:
        return True

    if tags.get("healthcare") == "hospital":
        return True

    return False


def fetch_hospitals():
    query = """
    [out:json];
    area["name:en"="Baku"]->.searchArea;
    (
      node["amenity"="hospital"](area.searchArea);
      way["amenity"="hospital"](area.searchArea);
    );
    out center;
    """

    response = requests.get(OVERPASS_URL, params={"data": query})
    response.raise_for_status()
    return response.json()["elements"]


def build_csv():
    elements = fetch_hospitals()
    hospitals = []

    for el in elements:
        tags = el.get("tags", {})
        name = tags.get("name")

        if not name:
            continue

        name_lower = name.lower()

        if any(bad in name_lower for bad in BLACKLIST):
            continue

        if not is_emergency_capable(tags):
            continue

        # Get coordinates
        lat = el.get("lat")
        lon = el.get("lon")

        if not lat and "center" in el:
            lat = el["center"]["lat"]
            lon = el["center"]["lon"]

        if not lat or not lon:
            continue

        hospitals.append({
            "name": name,
            "safe_name": safe_filename(name),
            "lat": lat,
            "lon": lon
        })



    with open("data/hospitals.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["name", "safe_name", "lat", "lon"]
        )
        writer.writeheader()
        writer.writerows(hospitals)


build_csv()

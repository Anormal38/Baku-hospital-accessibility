import requests
import json
import os

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

def fetch_baku_boundary():
    query = """
    [out:json];
    relation
      ["boundary"="administrative"]
      ["name:en"="Baku"];
    out geom;
    """

    r = requests.get(OVERPASS_URL, params={"data": query}, timeout=60)
    r.raise_for_status()
    data = r.json()

    if not data["elements"]:
        raise RuntimeError("No Baku boundary relation found")

    rel = data["elements"][0]


    coordinates = []

    for member in rel["members"]:
        if member["type"] == "way" and "geometry" in member:
            ring = [(p["lon"], p["lat"]) for p in member["geometry"]]
            coordinates.append([ring])

    geojson = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {
                "name": "Baku"
            },
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": coordinates
            }
        }]
    }

    os.makedirs("data", exist_ok=True)
    with open("data/baku_boundary.geojson", "w", encoding="utf-8") as f:
        json.dump(geojson, f)


fetch_baku_boundary()

import csv
import json
import time
import os
import requests

VALHALLA_URL = "https://valhalla1.openstreetmap.de/isochrone"
TIME_LIMIT = 10
MODES = {
    "car": "auto",
    "walk": "pedestrian"
}

DATA_DIR = "data/isochrones"

def get_isochrone(lat, lon, costing, max_retries=5):
    payload = {
        "locations": [{"lat": lat, "lon": lon}],
        "costing": costing,
        "contours": [{"time": TIME_LIMIT}],
        "polygons": True
    }

    for attempt in range(max_retries):
        response = requests.post(VALHALLA_URL, json=payload)

        if response.status_code == 200:
            return response.json()

        if response.status_code == 429:
            wait_time = 2 ** attempt
            time.sleep(wait_time)
            continue

        response.raise_for_status()

    raise RuntimeError("Valhalla rate limit exceeded after retries")


def load_hospitals(csv_path):
    hospitals = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            hospitals.append({
                "name": row["safe_name"],
                "lat": float(row["lat"]),
                "lon": float(row["lon"])
            })
    return hospitals

def save_isochrone(data, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f)

def main():
    hospitals = load_hospitals("data/hospitals.csv")

    for mode_name,costing in MODES.items():
        mode_dir = os.path.join(DATA_DIR, mode_name)
        os.makedirs(mode_dir, exist_ok=True)

        for hospital in hospitals:
            safe_name = hospital["name"].replace(" ", "_").lower()
            filename = f"{safe_name}_{TIME_LIMIT}min.json"
            filepath = os.path.join(mode_dir, filename)

            data = get_isochrone(
                hospital["lat"],
                hospital["lon"],
                costing
            )

            save_isochrone(data, filepath)

            time.sleep(1.05)

main()

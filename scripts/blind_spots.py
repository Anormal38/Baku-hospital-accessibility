import os
import json
import csv
import folium
from shapely.geometry import shape
from shapely.ops import unary_union
import geojson

ISO_DIR_CAR = "data/isochrones/car"
ISO_DIR_WALK = "data/isochrones/walk"

with open("data/baku_boundary.geojson", "r", encoding="utf-8") as f:
    baku_geo = json.load(f)

baku_polygon = shape(baku_geo["features"][0]["geometry"])

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

def load_clipped_isochrones(folder, boundary):
    clipped = []

    for file in os.listdir(folder):
        if not file.endswith(".json"):
            continue

        with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
            data = json.load(f)

        iso = shape(data["features"][0]["geometry"])
        iso_clipped = iso.intersection(boundary)

        if not iso_clipped.is_empty:
            clipped.append(iso_clipped)

    return clipped


car_polys = load_clipped_isochrones(ISO_DIR_CAR, baku_polygon)
walk_polys = load_clipped_isochrones(ISO_DIR_WALK, baku_polygon)

total_car = unary_union(car_polys)
total_walk = unary_union(walk_polys)

blind_car = baku_polygon.difference(total_car)
blind_walk = baku_polygon.difference(total_walk)

with open("data/blind_spots_car.geojson", "w", encoding="utf-8") as f:
    geojson.dump(geojson.Feature(geometry=blind_car, properties={}), f)

with open("data/blind_spots_walk.geojson", "w", encoding="utf-8") as f:
    geojson.dump(geojson.Feature(geometry=blind_walk, properties={}), f)

hospitals = load_hospitals("data/hospitals.csv")

def make_map(total_cov, blind_cov, filename):
    m = folium.Map(location=[40.4093, 49.8671], zoom_start=11)

    folium.GeoJson(
        baku_geo,
        style_function=lambda _: {
            "fillOpacity": 0,
            "color": "black",
            "weight": 2
        }
    ).add_to(m)

    folium.GeoJson(
        json.loads(json.dumps(total_cov.__geo_interface__)),
        style_function=lambda _: {
            "fillColor": "green",
            "color": "green",
            "fillOpacity": 0.25
        }
    ).add_to(m)

    folium.GeoJson(
        json.loads(json.dumps(blind_cov.__geo_interface__)),
        style_function=lambda _: {
            "fillColor": "red",
            "color": "red",
            "fillOpacity": 0.4
        }
    ).add_to(m)

    for h in hospitals:
        folium.CircleMarker(
            location=[h["lat"], h["lon"]],
            radius=5,
            color="blue",
            fill=True,
            fill_opacity=0.9,
            popup=h["name"]
        ).add_to(m)

    m.save(filename)


make_map(total_car, blind_car, "coverage_car.html")
make_map(total_walk, blind_walk, "coverage_walk.html")


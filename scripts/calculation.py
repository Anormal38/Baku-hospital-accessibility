import json
from shapely.geometry import shape
from pyproj import Geod

BAKU_BOUN_DIR = "data/baku_boundary.geojson"
BLIND_SPOTS_C = "data/blind_spots_car.geojson"
BLIND_SPOTS_W = "data/blind_spots_walk.geojson"

with open(BAKU_BOUN_DIR) as f:
    geojson_b = json.load(f)

with open(BLIND_SPOTS_C) as f:
    geojson_c = json.load(f)

with open(BLIND_SPOTS_W) as f:
    geojson_w = json.load(f)

geom_b = shape(geojson_b['features'][0]['geometry'])
geod_b = Geod(ellps="WGS84")

geom_c = shape(geojson_c["geometry"])
geod_c = Geod(ellps="WGS84")

geom_w = shape(geojson_w["geometry"])
geod_w = Geod(ellps="WGS84")

if geom_b.geom_type == "Polygon":
    area_b, _ = geod_b.geometry_area_perimeter(geom_b)
elif geom_b.geom_type == "MultiPolygon":
    area_b = sum(geod_b.geometry_area_perimeter(p)[0] for p in geom_b.geoms)

if geom_c.geom_type == "Polygon":
    area_c, _ = geod_c.geometry_area_perimeter(geom_c)
elif geom_c.geom_type == "MultiPolygon":
    area_c = sum(geod_c.geometry_area_perimeter(p)[0] for p in geom_c.geoms)

if geom_w.geom_type == "Polygon":
    area_w, _ = geod_w.geometry_area_perimeter(geom_w)
elif geom_w.geom_type == "MultiPolygon":
    area_w = sum(geod_w.geometry_area_perimeter(p)[0] for p in geom_w.geoms)

area_baku = abs(area_b/1000000)
area_car = abs(area_c/1000000)
area_walk = abs(area_w/1000000)

print(f"{area_baku}")
print(f"{area_car}, {(area_car/area_baku)*100}%")
print(f"{area_walk}, {(area_walk/area_baku)*100}%")

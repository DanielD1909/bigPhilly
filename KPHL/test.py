import json
import ijson
from shapely.geometry import Polygon, Point

# ---- CONFIG ----
input_file = "buildings_index.json"
output_file = "buildings_filtered.json"

# Replace with your bounding polygon coordinates
polygon_coords = [
    (
        -75.749962,
        39.431611
    ),
    (
        -75.667191,
        39.408218
    ),
    (
        -75.610664,
        39.402498
    ),
    (
        -75.559521,
        39.448241
    ),
    (
        -75.561138,
        39.602216
    ),
    (
        -75.532018,
        39.625462
    ),
    (
        -75.505424,
        39.623492
    ),
    (
        -75.500992,
        39.635046
    ),
    (
        -75.512073,
        39.642135
    ),
    (
        -75.477443,
        39.668016
    ),
    (
        -75.437961,
        39.701152
    ),
    (
        -75.339952,
        39.679722
    ),
    (
        -75.274269,
        39.700089
    ),
    (
        -75.171762,
        39.676452
    ),
    (
        -75.116252,
        39.632316
    ),
    (
        -75.069419,
        39.520424
    ),
    (
        -75.106885,
        39.493232
    ),
    (
        -75.253286,
        39.475391
    ),
    (
        -75.285022,
        39.443603
    ),
    (
        -75.278133,
        39.41641
    ),
    (
        -75.059166,
        39.348525
    ),
    (
        -74.954494,
        39.36713
    ),
    (
        -74.893135,
        39.508367
    ),
    (
        -74.967729,
        39.577023
    ),
    (
        -75.012244,
        39.666915
    ),
    (
        -74.952088,
        39.685435
    ),
    (
        -74.872682,
        39.732638
    ),
    (
        -74.857004,
        39.778377
    ),
    (
        -74.907853,
        39.814111
    ),
    (
        -74.899171,
        39.869818
    ),
    (
        -74.786268,
        39.893676
    ),
    (
        -74.718685,
        40.007506
    ),
    (
        -74.638605,
        40.079797
    ),
    (
        -74.686,
        40.118083
    ),
    (
        -74.639305,
        40.133912
    ),
    (
        -74.612714,
        40.159201
    ),
    (
        -74.579072,
        40.168659
    ),
    (
        -74.518815,
        40.19702
    ),
    (
        -74.507921,
        40.242071
    ),
    (
        -74.47019,
        40.252969
    ),
    (
        -74.467987,
        40.273859
    ),
    (
        -74.483023,
        40.271986
    ),
    (
        -74.509054,
        40.299709
    ),
    (
        -74.52109,
        40.303438
    ),
    (
        -74.548844,
        40.336662
    ),
    (
        -74.659784,
        40.380283
    ),
    (
        -74.768455,
        40.362925
    ),
    (
        -75.244454,
        40.42998
    ),
    (
        -75.453022,
        40.340982
    ),
    (
        -75.689061,
        40.259627
    ),
    (
        -75.922919,
        39.984571
    ),
    (
        -76.01078,
        39.781904
    ),
    (
        -76.007964,
        39.748642
    ),
    (
        -75.848889,
        39.712915
    ),
    (
        -75.874228,
        39.631648
    ),
    (
        -75.868597,
        39.570907
    ),
    (
        -75.749962,
        39.431611
    )
]
boundary_polygon = Polygon(polygon_coords)
# -----------------

# Load JSON
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# The buildings list is under "buildings"
buildings_list = data.get("buildings", [])

kept_buildings = []

for b in buildings_list:
    # Make sure b is a dict and has 'b' key
    if not isinstance(b, dict) or "b" not in b:
        continue

    minlon, minlat, maxlon, maxlat = b["b"]

    # Four corners of building bbox
    corners = [
        (minlon, minlat),
        (minlon, maxlat),
        (maxlon, minlat),
        (maxlon, maxlat),
    ]

    # Keep building if all corners inside polygon
    if all(boundary_polygon.covers(Point(c)) for c in corners):
        kept_buildings.append(b)

# Replace buildings in the JSON object
data["buildings"] = kept_buildings

# Write filtered output
with open(output_file, "w", encoding="utf-8") as out:
    json.dump(data, out, separators=(',', ':'))

print(f"Kept {len(kept_buildings)} of {len(buildings_list)} buildings")
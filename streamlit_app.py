import streamlit as st
import requests
import pandas as pd
import pydeck as pdk

st.title("🌳 Tree Map (New York)")
st.markdown("Visualizing tree data with options for density and canopy coverage.")

# Sidebar for user controls
with st.sidebar:
    st.header("Map Controls")
    view_option = st.radio("Select View", ["Tree Density", "Tree Canopy Coverage"])
    zoom_level = st.slider("Zoom Level", 10, 18, 12)
    radius = st.slider("Hexagon Radius (meters)", 100, 1000, 200)
    elevation_scale = st.slider("Elevation Scale", 10, 100, 20)
    pitch = 45 if view_option == "Tree Density" else 0  # 3D for density, 2D for canopy
    bearing = st.slider("Map Bearing", 0, 360, 0)

st.markdown("### How Elevation is Calculated")
st.markdown("""
For **Tree Density**, the elevation in the hexagonal grid is determined based on the number of trees within each hexagon. 
For **Tree Canopy Coverage**, estimated canopy coverage is calculated by buffering each tree point with an assumed average canopy radius (e.g., 5 meters).
For **Forest Areas**, OSM multipolygon data is used to display larger tree-covered regions.

- **Elevation Scale**: Controls the height of the hexagons based on density.
- **Radius**: Defines the area each hexagon covers.

Higher density areas will have more intense colors in the heatmap.
""")

# Overpass API endpoint
url = "http://overpass-api.de/api/interpreter"

# Overpass Query for Trees in New York
query_trees = """
[out:json];
(
  node["natural"="tree"](40.70,-74.00,40.80,-73.90);
);
out;
"""

# Overpass Query for Forest Areas in New York
query_forest = """
[out:json];
(
  way["landuse"="forest"](40.70,-74.00,40.80,-73.90);
  relation["landuse"="forest"](40.70,-74.00,40.80,-73.90);
  way["natural"="wood"](40.70,-74.00,40.80,-73.90);
  relation["natural"="wood"](40.70,-74.00,40.80,-73.90);
);
out geom;
"""

# Fetch tree data
st.info("Fetching tree data from Overpass API...")
response_trees = requests.get(url, params={"data": query_trees})
response_forest = requests.get(url, params={"data": query_forest})

tree_locations = []
forest_polygons = []
df_trees = pd.DataFrame()

if response_trees.status_code == 200:
    data_trees = response_trees.json()
    tree_locations = [
        {"lat": element["lat"], "lon": element["lon"]}
        for element in data_trees.get("elements", [])
    ]
    df_trees = pd.DataFrame(tree_locations)

if response_forest.status_code == 200:
    data_forest = response_forest.json()
    for element in data_forest.get("elements", []):
        if "geometry" in element:
            forest_polygons.append({
                "path": [[point["lon"], point["lat"]] for point in element["geometry"]]
            })

st.write(f"Total Trees: {len(df_trees)}")
st.write(f"Total Forest Polygons: {len(forest_polygons)}")

def create_layer():
    hex_layer = pdk.Layer(
        "HexagonLayer",
        df_trees,
        get_position=["lon", "lat"],
        radius=radius,
        elevation_scale=elevation_scale,
        elevation_range=[0, 1000],
        extruded=True,
        coverage=1,
        color_range=[
            [0, 50, 0], [100, 200, 100], [150, 255, 150],
            [255, 255, 100], [255, 100, 50], [255, 0, 0]
        ],
        pickable=True,
    )
    canopy_layer = pdk.Layer(
        "ScatterplotLayer",
        df_trees,
        get_position=["lon", "lat"],
        get_radius=5,  # Approximate canopy radius in meters
        get_fill_color=[0, 0, 200, 0],  # Blue semi-transparent
        pickable=True,
    )
    forest_layer = pdk.Layer(
        "PolygonLayer",
        forest_polygons,
        get_polygon="path",
        get_fill_color=[34, 139, 34, 100],  # Forest green with transparency
        pickable=True,
    )
    if view_option == "Tree Density":
        return [hex_layer]
    elif view_option == "Tree Canopy Coverage":
        return [forest_layer, canopy_layer]
    return []

# Pydeck visualization
if not df_trees.empty or forest_polygons:
    layers = create_layer()
    view_state = pdk.ViewState(
        longitude=df_trees["lon"].mean() if not df_trees.empty else -73.95,
        latitude=df_trees["lat"].mean() if not df_trees.empty else 40.75,
        zoom=zoom_level,
        pitch=pitch,
        bearing=bearing,
    )

    deck = pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/light-v10",
        tooltip={
            "html": "<b>Tree Data:</b> {elevationValue}",
            "style": {"backgroundColor": "steelblue", "color": "white"}
        }
    )

    st.pydeck_chart(deck)

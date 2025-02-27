import streamlit as st
import requests
import pandas as pd
import pydeck as pdk

st.title("🌳 Tree Density Map (New York)")
st.markdown("Visualizing tree density using a hexagonal grid.")

# Sidebar for user controls
radius = 200
elevation_scale = 20
with st.sidebar:
    st.header("Map Controls")
    zoom_level = st.slider("Zoom Level", 10, 18, 12)
    # radius = st.slider("Hexagon Radius (meters)", 100, 1000, 200)
    # elevation_scale = st.slider("Elevation Scale", 10, 100, 20)
    pitch = st.slider("Map Pitch", 0, 60, 45)
    bearing = st.slider("Map Bearing", 0, 360, 0)
    
st.markdown("### How Elevation is Calculated")
st.markdown("""
The elevation in the hexagonal grid is determined based on the density of trees within each hexagon. 
The more trees found within a hexagon's radius, the higher its elevation.
- **Elevation Range**: Limits the minimum and maximum height.

Higher density areas will have taller hexagons, while lower density areas will be shorter.
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

query_boundary = """
[out:json];
(
  relation["admin_level"="4"](40.70,-74.00,40.80,-73.90);
);
out geom;
"""

# Fetch tree data
st.info("Fetching tree and boundary data from Overpass API...")
response_trees = requests.get(url, params={"data": query_trees})
response_boundary = requests.get(url, params={"data": query_boundary})

tree_locations = []
boundary_polygons = []

if response_trees.status_code == 200:
    data_trees = response_trees.json()
    tree_locations = [
        {"lat": element["lat"], "lon": element["lon"]}
        for element in data_trees.get("elements", [])
    ]

df_trees = pd.DataFrame(tree_locations)

if response_boundary.status_code == 200:
    data_boundary = response_boundary.json()
    boundary_polygons = [
        {"path": [[node["lon"], node["lat"]] for node in way["geometry"]]}
        for way in data_boundary.get("elements", []) if "geometry" in way
    ]

df_boundary = pd.DataFrame(boundary_polygons)

# Pydeck visualization
if not df_trees.empty:
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
    
    boundary_layer = pdk.Layer(
        "PolygonLayer",
        df_boundary,
        get_polygon="path",
        get_fill_color=[200, 200, 200, 50],
        get_line_color=[0, 0, 0],
        line_width_min_pixels=2,
        pickable=True,
    )

    view_state = pdk.ViewState(
        longitude=df_trees["lon"].mean(),
        latitude=df_trees["lat"].mean(),
        zoom=zoom_level,
        pitch=pitch,
        bearing=bearing,
    )

    deck = pdk.Deck(
        layers=[hex_layer, boundary_layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/light-v10",
        tooltip={
            "html": "<b>Tree Density:</b> {elevationValue}",
            "style": {"backgroundColor": "steelblue", "color": "white"}
        }
    )

    st.pydeck_chart(deck)

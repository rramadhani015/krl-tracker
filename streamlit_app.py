import streamlit as st
import requests
import pandas as pd
import pydeck as pdk

st.title("🌳 Tree Density Map (New York)")
st.markdown("Visualizing tree density using a hexagonal grid.")

# Sidebar for user controls
with st.sidebar:
    st.header("Map Controls")
    zoom_level = st.slider("Zoom Level", 10, 18, 12)
    pitch = st.slider("Map Pitch", 0, 60, 45)
    bearing = st.slider("Map Bearing", 0, 360, 0)

# Overpass API endpoint
url = "http://overpass-api.de/api/interpreter"

# Overpass Query for Trees in New York
query = """
[out:json];
(
  node["natural"="tree"](40.70,-74.00,40.80,-73.90);
);
out;
"""

# Fetch data from Overpass API
st.info("Fetching tree data from Overpass API...")
response = requests.get(url, params={"data": query})

if response.status_code == 200:
    data = response.json()
    
    # Extract latitude & longitude
    tree_locations = [
        {"lat": element["lat"], "lon": element["lon"]}
        for element in data.get("elements", [])
    ]
    
    if tree_locations:
        df = pd.DataFrame(tree_locations)
        st.success(f"Total Trees Found: {len(df)}")
    else:
        st.warning("No tree data found.")
        df = pd.DataFrame(columns=["lat", "lon"])
else:
    st.error("Failed to fetch data from Overpass API.")
    df = pd.DataFrame(columns=["lat", "lon"])

# Pydeck visualization
if not df.empty:
    hex_layer = pdk.Layer(
        "HexagonLayer",
        df,
        get_position=["lon", "lat"],
        radius=radius,
        elevation_scale=elevation_scale,
        elevation_range=[0, 1000],
        extruded=True,
        coverage=1,
        color_range=[
            [0, 50, 0], [100, 200, 100], [150, 255, 150],
            [255, 255, 100], [255, 100, 50], [255, 0, 0]
        ]
    )

    view_state = pdk.ViewState(
        longitude=df["lon"].mean(),
        latitude=df["lat"].mean(),
        zoom=zoom_level,
        pitch=pitch,
        bearing=bearing,
    )

    deck = pdk.Deck(
        layers=[hex_layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/light-v10",
    )

    st.pydeck_chart(deck)

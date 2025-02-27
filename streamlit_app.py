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
        ],
        pickable=True,
    )
    
    text_layer = pdk.Layer(
        "TextLayer",
        df,
        get_position=["lon", "lat"],
        get_text="Tree Density",
        get_size=12,
        get_color=[255, 255, 255],
        get_angle=0,
        pickable=True,
        background=True
    )
    
    # Tooltip Pin Layer
    pin_layer = pdk.Layer(
        "ScatterplotLayer",
        df,
        get_position=["lon", "lat"],
        get_fill_color=[255, 0, 0],  # Red pin
        get_radius=50,
        pickable=True,
    )

    view_state = pdk.ViewState(
        longitude=df["lon"].mean(),
        latitude=df["lat"].mean(),
        zoom=zoom_level,
        pitch=pitch,
        bearing=bearing,
    )

    deck = pdk.Deck(
        layers=[hex_layer, text_layer, pin_layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/light-v10",
        tooltip={
            "html": "<b>Tree Density:</b> {elevationValue}",
            "style": {"backgroundColor": "steelblue", "color": "white"}
        }
    )

    st.pydeck_chart(deck)

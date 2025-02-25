import streamlit as st
import pydeck as pdk

# 🔑 Enter your Mapbox token (replace with your actual token)
MAPBOX_TOKEN = "pk.eyJ1IjoicmFtYWRoYW5pMDE1IiwiYSI6ImNpeHo1ZTU4eTAwNXAzM3J5YTB0cndteWIifQ.TfUY-zPT2r6bdci0vc7FCA"

# 🔍 Select location
regions = {
    "Mount Merapi": [110.44, -7.54],  # [Longitude, Latitude]
    "Mount Bromo": [112.95, -7.92],
    "Jakarta": [106.85, -6.2]
}

selected_region = st.selectbox("Select a region:", list(regions.keys()))
longitude, latitude = regions[selected_region]

# 📌 Define Pydeck Map
view_state = pdk.ViewState(
    longitude=longitude,
    latitude=latitude,
    zoom=10,
    pitch=60,
    bearing=0,
)

# 🗺️ Mapbox Terrain Layer
terrain_layer = pdk.Layer(
    "TerrainLayer",
    data=[],
    elevation_data="mapbox://mapbox.terrain-rgb",
    texture="mapbox://mapbox.satellite",
    elevation_decoder={
        "rScaler": 65536,  # Previously 256
        "gScaler": 256, 
        "bScaler": 1, 
        "offset": -10000  # Previously -32768
    },
    bounds=[longitude - 0.1, latitude - 0.1, longitude + 0.1, latitude + 0.1],
)

# 🏔️ Render in Streamlit
st.pydeck_chart(pdk.Deck(
    layers=[terrain_layer],
    initial_view_state=view_state,
    map_provider="mapbox",
    map_style="mapbox://styles/mapbox/satellite-streets-v11",
    api_keys={"mapbox": MAPBOX_TOKEN},
))

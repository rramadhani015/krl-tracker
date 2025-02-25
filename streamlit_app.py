import streamlit as st
import numpy as np
import requests
from io import BytesIO
from PIL import Image
import pydeck as pdk

# 🔑 Enter your Mapbox token (replace with your actual token)
MAPBOX_TOKEN = "pk.eyJ1IjoicmFtYWRoYW5pMDE1IiwiYSI6ImNtN2p6N21oaDBhaDcyanMzMHRiNjJsOTEifQ.tS3O3ERXLBjrqlfYep2OLQ"

# 🔍 Select a test region
regions = {
    "Mount Merapi": [110.44, -7.54],  # [Longitude, Latitude]
    "Mount Bromo": [112.95, -7.92],
    "Jakarta": [106.85, -6.2]
}
selected_region = st.selectbox("Select a region:", list(regions.keys()))
longitude, latitude = regions[selected_region]

# 🏔️ Mapbox Terrain-RGB API (Template URL)
TERRAIN_URL = f"https://api.mapbox.com/v4/mapbox.terrain-rgb/{{z}}/{{x}}/{{y}}.pngraw?access_token={MAPBOX_TOKEN}"

# 📌 Pydeck 3D View
view_state = pdk.ViewState(
    longitude=longitude,
    latitude=latitude,
    zoom=10,
    pitch=60,
    bearing=0,
)

# 🏔️ Mapbox Terrain Layer
terrain_layer = pdk.Layer(
    "TerrainLayer",
    data=[],
    elevation_data=TERRAIN_URL,  # 🔥 Using Mapbox Terrain-RGB API
    elevation_decoder={
        "rScaler": 256, "gScaler": 1, "bScaler": 1/256, "offset": -32768  # Mapbox Terrain-RGB decoding
    },
    bounds=[longitude - 1, latitude - 1, longitude + 1, latitude + 1],
)

# 🌍 Render Mapbox 3D Terrain in Pydeck
st.pydeck_chart(pdk.Deck(
    layers=[terrain_layer],
    initial_view_state=view_state,
    map_provider="mapbox",
    map_style="mapbox://styles/mapbox/satellite-streets-v11",  # 🛰️ Use Mapbox Satellite Terrain
    # mapbox_key=MAPBOX_TOKEN  # ✅ Ensure Mapbox API Key is included
))



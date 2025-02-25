import streamlit as st
import pydeck as pdk

# 🔑 Your Mapbox API Key
MAPBOX_TOKEN = "your_actual_mapbox_api_key"

# 📌 Select a test location
regions = {
    "Mount Merapi": [110.44, -7.54, 10],  
    "Mount Bromo": [112.95, -7.92, 11],
    "Jakarta": [106.85, -6.2, 10]
}
selected_region = st.selectbox("Select a region:", list(regions.keys()))
longitude, latitude, zoom = regions[selected_region]

# 🏔️ Pydeck 3D Terrain Layer
terrain_layer = pdk.Layer(
    "TerrainLayer",
    elevation_decoder={
        "rScaler": 256, "gScaler": 256, "bScaler": 256, "offset": 0
    },
    texture="https://basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}.png",
    elevation_data="https://api.mapbox.com/v4/mapbox.terrain-rgb/{z}/{x}/{y}.pngraw?access_token=" + MAPBOX_TOKEN
)

# 🗺️ Pydeck View
view_state = pdk.ViewState(
    longitude=longitude,
    latitude=latitude,
    zoom=zoom,
    pitch=60,
    bearing=30
)

# 🎨 Render the map in Streamlit
st.pydeck_chart(pdk.Deck(
    layers=[terrain_layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/satellite-streets-v12",
    api_keys={"mapbox": MAPBOX_TOKEN}
))

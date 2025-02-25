import streamlit as st
import pydeck as pdk

# 🔑 Your Mapbox API Key (replace with your real key)
MAPBOX_TOKEN = "pk.eyJ1IjoicmFtYWRoYW5pMDE1IiwiYSI6ImNtN2p6N21oaDBhaDcyanMzMHRiNjJsOTEifQ.tS3O3ERXLBjrqlfYep2OLQ"

# 📍 Locations in Indonesia
locations = {
    "Mount Merapi, Indonesia": [110.44, -7.54, 10],
    "Mount Bromo, Indonesia": [112.95, -7.92, 11],
    "Jakarta, Indonesia": [106.85, -6.2, 10]
}

# 🎯 Select a location
selected_location = st.selectbox("Choose a location:", list(locations.keys()))
longitude, latitude, zoom = locations[selected_location]

# 🎨 **Use a colored terrain basemap** (instead of grayscale Terrain-RGB)
terrain_colored_basemap = "mapbox://styles/mapbox/outdoors-v11"

# 🏔️ **3D Terrain Layer**
terrain_layer = pdk.Layer(
    "TerrainLayer",
    elevation_data=f"https://api.mapbox.com/v4/mapbox.terrain-rgb/{{z}}/{{x}}/{{y}}.pngraw?access_token={MAPBOX_TOKEN}",
    elevation_decoder={"rScaler": 65536, "gScaler": 256, "bScaler": 1, "offset": 0},
    bounds=[longitude - 1, latitude - 1, longitude + 1, latitude + 1]
)

# 📌 View Configuration
view_state = pdk.ViewState(
    longitude=longitude,
    latitude=latitude,
    zoom=zoom,
    pitch=60,
    bearing=30,
    min_zoom=5,
    max_zoom=15
)

# 🗺️ Render the 3D Map with the colored terrain
st.pydeck_chart(pdk.Deck(
    layers=[terrain_layer],
    initial_view_state=view_state,
    map_style=terrain_colored_basemap,  # ✅ Pre-colored basemap for better visualization
    api_keys={"mapbox": MAPBOX_TOKEN}
))


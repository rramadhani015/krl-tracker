import streamlit as st
import pydeck as pdk

# 🔑 Your Mapbox API Key (replace with your real key)
MAPBOX_TOKEN = "pk.eyJ1IjoicmFtYWRoYW5pMDE1IiwiYSI6ImNtN2p6N21oaDBhaDcyanMzMHRiNjJsOTEifQ.tS3O3ERXLBjrqlfYep2OLQ"

# 🎯 Locations in Indonesia
locations = {
    "Mount Merapi, Indonesia": [110.44, -7.54, 10],
    "Mount Bromo, Indonesia": [112.95, -7.92, 11],
    "Jakarta, Indonesia": [106.85, -6.2, 10]
}

# 📍 Select a location
selected_location = st.selectbox("Choose a location:", list(locations.keys()))
longitude, latitude, zoom = locations[selected_location]

# 🎨 **Color ramp for elevation**
elevation_color_ramp = [
    [0, [242, 239, 233]],       # Lowland
    [500, [205, 174, 112]],     # Hills
    [1000, [160, 112, 65]],     # Mountains
    [2000, [100, 64, 40]],      # Higher elevation
    [3000, [60, 40, 25]],       # Peaks
]

# 🏔️ **3D Terrain Layer with colorized elevation**
terrain_layer = pdk.Layer(
    "TerrainLayer",
    elevation_data=f"https://api.mapbox.com/v4/mapbox.terrain-rgb/{{z}}/{{x}}/{{y}}.pngraw?access_token={MAPBOX_TOKEN}",
    elevation_decoder={"rScaler": 65536, "gScaler": 256, "bScaler": 1, "offset": 0},
    texture=f"https://api.mapbox.com/styles/v1/mapbox/outdoors-v11/tiles/{{z}}/{{x}}/{{y}}?access_token={MAPBOX_TOKEN}",  # Adds realistic terrain color
    color=elevation_color_ramp,
    bounds=[longitude - 1, latitude - 1, longitude + 1, latitude + 1]
)

# 📌 3D View Configuration
view_state = pdk.ViewState(
    longitude=longitude,
    latitude=latitude,
    zoom=zoom,
    pitch=60,
    bearing=30,
    min_zoom=5,
    max_zoom=15
)

# 🗺️ Render the map with custom colors
st.pydeck_chart(pdk.Deck(
    layers=[terrain_layer],
    initial_view_state=view_state,
    map_style=None,  # ❌ No basemap, just colorized terrain
    api_keys={"mapbox": MAPBOX_TOKEN}
))


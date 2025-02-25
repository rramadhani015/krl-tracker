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

# 🎨 Define the color ramp (low elevation = green, high elevation = white)
color_ramp = [
    [0, [34, 139, 34]],  # Low elevation → Green
    [500, [110, 204, 57]],  # Slightly higher → Light green
    [1000, [255, 255, 102]],  # Medium → Yellow
    [2000, [255, 165, 0]],  # Higher → Orange
    [3000, [255, 69, 0]],  # Very high → Red
    [4000, [255, 255, 255]]  # Highest → White
]

# 🏔️ **TerrainLayer** for 3D elevation
terrain_layer = pdk.Layer(
    "TerrainLayer",
    elevation_data=f"https://api.mapbox.com/v4/mapbox.terrain-rgb/{{z}}/{{x}}/{{y}}.pngraw?access_token={MAPBOX_TOKEN}",
    elevation_decoder={"rScaler": 65536, "gScaler": 256, "bScaler": 1, "offset": 0},
    bounds=[longitude - 1, latitude - 1, longitude + 1, latitude + 1],
    texture=f"https://api.mapbox.com/styles/v1/mapbox/outdoors-v11/static/{longitude},{latitude},{zoom},0,0/500x500?access_token={MAPBOX_TOKEN}"
)

# 🌍 **BitmapLayer** to overlay colorized DEM
bitmap_layer = pdk.Layer(
    "BitmapLayer",
    bounds=[longitude - 1, latitude - 1, longitude + 1, latitude + 1],
    image=f"https://api.mapbox.com/v4/mapbox.terrain-rgb/{{z}}/{{x}}/{{y}}.pngraw?access_token={MAPBOX_TOKEN}",
    pickable=False,
    opacity=0.6
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

# 🗺️ Render the map
st.pydeck_chart(pdk.Deck(
    layers=[terrain_layer, bitmap_layer],
    initial_view_state=view_state,
    map_style=None,  # No basemap
    api_keys={"mapbox": MAPBOX_TOKEN}
))

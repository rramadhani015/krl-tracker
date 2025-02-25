import streamlit as st
import pydeck as pdk

# 🔑 Your Mapbox API Key (replace with your real key)
MAPBOX_TOKEN = "pk.eyJ1IjoicmFtYWRoYW5pMDE1IiwiYSI6ImNtN2p6N21oaDBhaDcyanMzMHRiNjJsOTEifQ.tS3O3ERXLBjrqlfYep2OLQ"

# 📌 Define locations with lat, lon, and zoom levels
locations = {
    "Mount Merapi, Indonesia": [110.44, -7.54, 10],
    "Mount Bromo, Indonesia": [112.95, -7.92, 11],
    "Jakarta, Indonesia": [106.85, -6.2, 10]
}

# 🌍 Select a location
selected_location = st.selectbox("Choose a location:", list(locations.keys()))
longitude, latitude, zoom = locations[selected_location]

# 🏔️ Pydeck TerrainLayer (Full 3D)
terrain_layer = pdk.Layer(
    "TerrainLayer",
    elevation_decoder={
        "rScaler": 65536,  # Scale for red channel
        "gScaler": 256,     # Scale for green channel
        "bScaler": 1,       # Scale for blue channel
        "offset": 0         # Offset for elevation values
    },
    elevation_data=f"https://api.mapbox.com/v4/mapbox.terrain-rgb/{{z}}/{{x}}/{{y}}.pngraw?access_token={MAPBOX_TOKEN}",
    texture="https://basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}.png",
    bounds=[-180, -85.0511, 180, 85.0511]  # Global bounds
)

# 🗺️ Pydeck View Configuration
view_state = pdk.ViewState(
    longitude=longitude,
    latitude=latitude,
    zoom=zoom,
    pitch=60,  # Tilt for 3D effect
    bearing=30
)

# 🗺️ Render 3D Terrain in Streamlit
st.pydeck_chart(pdk.Deck(
    layers=[terrain_layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/satellite-streets-v12",
    api_keys={"mapbox": MAPBOX_TOKEN}
))

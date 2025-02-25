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

# 🏔️ Pydeck TerrainLayer (Fix for Sticking Issue)
terrain_layer = pdk.Layer(
    "TerrainLayer",
    elevation_decoder={
        "rScaler": 65536,
        "gScaler": 256,
        "bScaler": 1,
        "offset": 0
    },
    elevation_data=f"https://api.mapbox.com/v4/mapbox.terrain-rgb/{{z}}/{{x}}/{{y}}.pngraw?access_token={MAPBOX_TOKEN}",
    texture="https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v12/tiles/256/{z}/{x}/{y}?access_token=" + MAPBOX_TOKEN,
    bounds=[longitude - 1, latitude - 1, longitude + 1, latitude + 1],  # Smaller bounds to prevent gaps
)

# 🗺️ Pydeck View Configuration (Fix for Zooming Issue)
view_state = pdk.ViewState(
    longitude=longitude,
    latitude=latitude,
    zoom=zoom,
    min_zoom=5,  # Prevent zooming out too much
    max_zoom=15,  # Prevent excessive zoom causing terrain gaps
    pitch=60,
    bearing=30
)

# 🗺️ Render 3D Terrain in Streamlit
st.pydeck_chart(pdk.Deck(
    layers=[terrain_layer],
    initial_view_state=view_state,
    map_style=None,  # No additional map style to avoid conflict
    api_keys={"mapbox": MAPBOX_TOKEN}
))
# 🗺️ Render 3D Terrain in Streamlit
st.pydeck_chart(pdk.Deck(
    layers=[terrain_layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/satellite-streets-v12",
    api_keys={"mapbox": MAPBOX_TOKEN}
))

import streamlit as st
import pydeck as pdk

# Mapbox Access Token (Replace with your own)
MAPBOX_API_KEY = "pk.eyJ1IjoicmFtYWRoYW5pMDE1IiwiYSI6ImNtN2p6N21oaDBhaDcyanMzMHRiNjJsOTEifQ.tS3O3ERXLBjrqlfYep2OLQ"

# Sidebar controls
st.sidebar.header("Map Controls")
pitch = st.sidebar.slider("Pitch", min_value=0, max_value=60, value=60, step=5)
bearing = st.sidebar.slider("Bearing", min_value=0, max_value=360, value=0, step=5)

# Define the viewport for the map
view = pdk.ViewState(
    latitude=32.7213,  # Example location
    longitude=-114.26608,
    zoom=12,
    pitch=pitch,
    bearing=bearing
)

# Define the terrain layer using Mapbox DEM Raster Tiles
terrain_layer = pdk.Layer(
    "TerrainLayer",
    data=None,  # No input data required for raster layers
    elevation_decoder={"rScaler": 256, "gScaler": 1, "bScaler": 1 / 256, "offset": -32768},
    # elevation_data="mapbox://mapbox.mapbox-terrain-dem-v1",
    # elevation_data="https://api.mapbox.com/v4/mapbox.terrain-rgb/{zoom}/{x}/{y}{@2x}.pngraw?access_token="+ MAPBOX_API_KEY,
    elevation_data="https://api.mapbox.com/v4/mapbox.terrain-rgb/{zoom}/{x}/{y}{@2x}.pngraw?access_token="+ MAPBOX_API_KEY,
    texture="https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/256/{z}/{x}/{y}?access_token=" + MAPBOX_API_KEY,
    exaggeration=1.5,
    bounds=[-115, 32, -113, 34],  # Define bounding box for visualization
    material={"ambient": 0.5, "diffuse": 0.5, "shininess": 0.5, "specularColor": [255, 255, 255]},
)

# Create the deck with the terrain layer
deck = pdk.Deck(
    layers=[terrain_layer],
    initial_view_state=view,
    map_provider="mapbox",
    map_style="mapbox://styles/mapbox/satellite-streets-v12",
)

# Display in Streamlit
st.pydeck_chart(deck)

import streamlit as st
import numpy as np
import requests
from io import BytesIO
from PIL import Image
import pydeck as pdk

# Streamlit title
# st.title("🌍 3D Terrain Visualization with Color Ramp")

# # Select a region for the DEM
# regions = {
#     "Mount Merapi": (110.36, -7.54, 110.50, -7.40),
#     "Mount Bromo": (112.92, -7.95, 113.0, -7.85),
#     "Jakarta": (106.75, -6.2, 106.9, -6.0),
# }

# selected_region = st.selectbox("Select a region:", list(regions.keys()))
# west, south, east, north = regions[selected_region]

# # Define the AWS Terrarium DEM tile URL
# zoom = 10  # Tile zoom level
# x_tile = 613  # Adjust for specific regions
# y_tile = 389  # Adjust for specific regions

# dem_url = f"https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{zoom}/{x_tile}/{y_tile}.png"

# # Function to fetch and decode DEM data
# def fetch_dem(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         return Image.open(BytesIO(response.content))
#     else:
#         st.error("❌ Failed to fetch DEM data")
#         return None

# # Fetch DEM data
# dem_image = fetch_dem(dem_url)

# if dem_image:
#     # Convert to NumPy array and decode elevation
#     dem_array = np.array(dem_image, dtype=np.int32)

#     # Decode elevation from Terrarium RGB format
#     elevation = (
#         dem_array[:, :, 0].astype(np.int32) * 256 +  # Red
#         dem_array[:, :, 1].astype(np.int32) +        # Green
#         dem_array[:, :, 2].astype(np.int32) / 256 - 32768  # Blue + Offset
#     )

#     # Normalize elevation for color mapping
#     min_elev, max_elev = np.min(elevation), np.max(elevation)
#     norm_elev = (elevation - min_elev) / (max_elev - min_elev)

#     # Define color gradient (Green -> Brown -> White)
#     elevation_color_scale = [
#         [0, [34, 139, 34]],      # Green (Low areas)
#         [500, [139, 69, 19]],    # Brown (Mid elevation)
#         [1500, [255, 255, 255]]  # White (High elevation)
#     ]

#     # Pydeck Terrain Layer
#     terrain_layer = pdk.Layer(
#         "TerrainLayer",
#         data=[],
#         elevation_data="https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png",
#         elevation_decoder={
#             "rScaler": 256,
#             "gScaler": 1,
#             "bScaler": 1/256,
#             "offset": -32768,
#         },
#         bounds=[west, south, east, north],
#         material={"ambient": 0.5, "diffuse": 0.6, "shininess": 10, "specularColor": [255, 255, 255]},
#     )

#     # GPUGridLayer to colorize the terrain based on elevation
#     color_layer = pdk.Layer(
#         "GPUGridLayer",
#         data=[],
#         get_position="[longitude, latitude]",
#         get_elevation="elevation",
#         get_color="color",
#         color_range=elevation_color_scale,
#         extruded=True,
#         cell_size=200,
#     )

#     # Define View
#     view_state = pdk.ViewState(
#         longitude=(west + east) / 2,
#         latitude=(south + north) / 2,
#         zoom=10,
#         pitch=50,
#     )

#     # Render in Streamlit
#     st.pydeck_chart(pdk.Deck(layers=[terrain_layer, color_layer], initial_view_state=view_state))


# # 🔑 Enter your Mapbox token (replace with your actual token)
MAPBOX_TOKEN = "pk.eyJ1IjoicmFtYWRoYW5pMDE1IiwiYSI6ImNtN2p6N21oaDBhaDcyanMzMHRiNjJsOTEifQ.tS3O3ERXLBjrqlfYep2OLQ"

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
# terrain_layer = pdk.Layer(
#     "TerrainLayer",
#     data=[],
#     elevation_data="mapbox://mapbox.terrain-rgb",
#     texture="mapbox://mapbox.satellite",
#     elevation_decoder={
#         "rScaler": 256,
#         "gScaler": 1,
#         "bScaler": 1/256,
#         "offset": -32768,
#     },
#     bounds=[longitude - 0.1, latitude - 0.1, longitude + 0.1, latitude + 0.1],
# )

# # 🏔️ Render in Streamlit
# st.pydeck_chart(pdk.Deck(
#     layers=[terrain_layer],
#     initial_view_state=view_state,
#     map_provider="mapbox",
#     map_style="mapbox://styles/mapbox/satellite-streets-v11",
#     api_keys={"mapbox": MAPBOX_TOKEN},
# ))


import streamlit as st

# 🔑 Your Mapbox API Key
MAPBOX_TOKEN = "pk.eyJ1IjoicmFtYWRoYW5pMDE1IiwiYSI6ImNtN2p6N21oaDBhaDcyanMzMHRiNjJsOTEifQ.tS3O3ERXLBjrqlfYep2OLQ"

# 📌 Select a test location
regions = {
    "Mount Merapi": [110.44, -7.54, 10],  # [Longitude, Latitude, Zoom]
    "Mount Bromo": [112.95, -7.92, 11],
    "Jakarta": [106.85, -6.2, 10]
}
selected_region = st.selectbox("Select a region:", list(regions.keys()))
longitude, latitude, zoom = regions[selected_region]

# 📜 HTML + JS for Mapbox GL JS 3D Terrain
map_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Mapbox GL JS 3D Terrain</title>
    <script src="https://api.mapbox.com/mapbox-gl-js/v2.14.0/mapbox-gl.js"></script>
    <link href="https://api.mapbox.com/mapbox-gl-js/v2.14.0/mapbox-gl.css" rel="stylesheet" />
    <style>
        body {{ margin: 0; padding: 0; }}
        #map {{ width: 100%; height: 100vh; }}
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        mapboxgl.accessToken = '{MAPBOX_TOKEN}';

        var map = new mapboxgl.Map({{
            container: 'map',
            style: 'mapbox://styles/mapbox/satellite-streets-v11',  // 🛰️ Use Satellite Terrain
            center: [{longitude}, {latitude}],  // 🔍 User-selected location
            zoom: {zoom},
            pitch: 60,  // 🔄 Tilt for 3D effect
            bearing: 0,
            antialias: true  // 📏 Smooth rendering
        }});

        // 🏔️ Enable 3D Terrain using Mapbox Terrain-RGB
        map.on('load', function () {{
            map.addSource('mapbox-dem', {{
                "type": "raster-dem",
                "url": "mapbox://mapbox.terrain-rgb",
                "tileSize": 512,
                "maxzoom": 14
            }});
            map.setTerrain({{
                "source": "mapbox-dem",
                "exaggeration": 1.5  // ⛰️ Elevation exaggeration for better visualization
            }});
        }});
    </script>
</body>
</html>
"""

# 🏔️ Embed Mapbox GL JS into Streamlit
st.components.v1.html(map_html, height=600)

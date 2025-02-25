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
<title>Add 3D terrain to a map</title>
<meta name="viewport" content="initial-scale=1,maximum-scale=1,user-scalable=no">
<link href="https://api.mapbox.com/mapbox-gl-js/v3.10.0/mapbox-gl.css" rel="stylesheet">
<script src="https://api.mapbox.com/mapbox-gl-js/v3.10.0/mapbox-gl.js"></script>
<style>
body { margin: 0; padding: 0; }
#map { position: absolute; top: 0; bottom: 0; width: 100%; }
</style>
</head>
<body>
<div id="map"></div>

<script>
	mapboxgl.accessToken = ''{MAPBOX_TOKEN}'';
    const map = new mapboxgl.Map({
        container: 'map',
        zoom: 14,
        center: [-114.26608, 32.7213],
        pitch: 80,
        bearing: 41,
        // Choose from Mapbox's core styles, or make your own style with Mapbox Studio
        style: 'mapbox://styles/mapbox/satellite-streets-v12'
    });

    map.on('style.load', () => {
        map.addSource('mapbox-dem', {
            'type': 'raster-dem',
            'url': 'mapbox://mapbox.mapbox-terrain-dem-v1',
            'tileSize': 512,
            'maxzoom': 14
        });
        // add the DEM source as a terrain layer with exaggerated height
        map.setTerrain({ 'source': 'mapbox-dem', 'exaggeration': 1.5 });
    });
</script>

</body>
</html>
"""

# 🏔️ Embed Mapbox GL JS into Streamlit
st.components.v1.html(map_html, height=600)

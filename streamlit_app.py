import streamlit as st
import requests
import folium
from streamlit_folium import folium_static
from streamlit_js_eval import get_geolocation
from geopy.distance import geodesic

# Title
st.title("📍 KRL Commuterline Tracker")

# Get real-time GPS
location = get_geolocation()

if location:
    st.success(f"Your location: {location}")

    lat, lon = location["latitude"], location["longitude"]
    st.success(f"Your location: {lat}, {lon}")

    # Fetch KRL stations from Overpass API
    @st.cache_data
    def get_krl_stations():
        overpass_url = "http://overpass-api.de/api/interpreter"
        query = """
        [out:json];
            node["railway"="station"]["network"="KAI Commuter"](around:50000,-6.2088,106.8456);
        out body;
        """
        response = requests.get(overpass_url, params={'data': query})
        if response.status_code == 200:
            data = response.json()
            return [(node["lat"], node["lon"], node["tags"].get("name", "Unknown Station")) for node in data.get("elements", [])]
        return []

    stations = get_krl_stations()

    if stations:
        # Find the two nearest stations
        def find_nearest_stations(lat, lon, stations):
            sorted_stations = sorted(stations, key=lambda s: geodesic((lat, lon), (s[0], s[1])).meters)
            return sorted_stations[:2] if len(sorted_stations) > 1 else sorted_stations

        nearest_stations = find_nearest_stations(lat, lon, stations)

        # Show nearest stations
        if len(nearest_stations) == 2:
            st.success(f"You are between **{nearest_stations[0][2]}** and **{nearest_stations[1][2]}**.")
        else:
            st.info(f"Nearest Station: **{nearest_stations[0][2]}**.")

        # Create map
        m = folium.Map(location=[lat, lon], zoom_start=13)
        folium.Marker([lat, lon], tooltip="You Are Here", icon=folium.Icon(color="blue")).add_to(m)

        # Add stations to map
        for station in stations:
            folium.Marker([station[0], station[1]], tooltip=station[2], icon=folium.Icon(color="red")).add_to(m)

        # Show map
        folium_static(m)

    else:
        st.error("No KRL stations found.")
else:
    st.warning("Waiting for GPS location... Please allow location access.")

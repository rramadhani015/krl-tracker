import streamlit as st
import requests
import folium
from streamlit_folium import folium_static
from streamlit_js_eval import get_geolocation
from geopy.distance import geodesic

st.title("📍 KRL Commuterline Tracker")

# Get real-time GPS location
location = get_geolocation()

if location and "coords" in location:
    lat, lon = location["coords"]["latitude"], location["coords"]["longitude"]
    st.success(f"Your location: {lat}, {lon}")

    # Fetch KRL stations
    @st.cache_data
    def get_krl_stations():
        overpass_url = "http://overpass-api.de/api/interpreter"
        query = """
        [out:json];
        (
            node["railway"="station"]["network"="KAI Commuter"](around:50000,-6.2088,106.8456);
            way["railway"="rail"]["network"="KAI Commuter"](around:50000,-6.2088,106.8456);
        );
        out body;
        >;
        out skel qt;
        """
        response = requests.get(overpass_url, params={'data': query})
        if response.status_code == 200:
            data = response.json()
            stations = {}
            ways = []
            
            for element in data["elements"]:
                if element["type"] == "node" and "tags" in element:
                    stations[element["id"]] = (
                        element["lat"], element["lon"], element["tags"].get("name", "Unknown Station")
                    )
                elif element["type"] == "way":
                    ways.append(element["nodes"])
            
            return stations, ways
        return {}, []

    stations, station_relations = get_krl_stations()

    if stations:
        # Find nearest stations
        def find_nearest_stations(lat, lon, stations):
            station_list = list(stations.values())
            sorted_stations = sorted(station_list, key=lambda s: geodesic((lat, lon), (s[0], s[1])).meters)
            return sorted_stations[:2] if len(sorted_stations) > 1 else sorted_stations

        nearest_stations = find_nearest_stations(lat, lon, stations)

        # Create map
        m = folium.Map(location=[lat, lon], zoom_start=13)

        # Add user location
        folium.Marker([lat, lon], tooltip="You Are Here", icon=folium.Icon(color="blue")).add_to(m)

        # Add stations
        for station_id, (s_lat, s_lon, s_name) in stations.items():
            folium.Marker([s_lat, s_lon], tooltip=s_name, icon=folium.Icon(color="red")).add_to(m)

        # Draw station relations (routes)
        for way in station_relations:
            route_coords = [(stations[n][0], stations[n][1]) for n in way if n in stations]
            if len(route_coords) > 1:
                folium.PolyLine(route_coords, color="green", weight=3, opacity=0.8).add_to(m)

        # Show nearest stations
        if len(nearest_stations) == 2:
            st.success(f"You are between **{nearest_stations[0][2]}** and **{nearest_stations[1][2]}**.")
        else:
            st.info(f"Nearest Station: **{nearest_stations[0][2]}**.")

        folium_static(m)

    else:
        st.error("No KRL stations found.")
else:
    st.warning("Waiting for GPS location... Please allow location access.")

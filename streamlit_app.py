import streamlit as st
import requests
import pydeck as pdk
from streamlit_js_eval import get_geolocation
from geopy.distance import geodesic

st.title("📍 Public Transport Tracker")

# Sidebar menu
option = st.sidebar.radio("Select Tracker:", ("KRL Tracker"))

# Get real-time GPS location
location = get_geolocation()

if location and "coords" in location:
    lat, lon = location["coords"]["latitude"], location["coords"]["longitude"]
    st.success(f"Your location: {lat}, {lon}")

    @st.cache_data
    def get_krl_data():
        overpass_url = "http://overpass-api.de/api/interpreter"
        query = """
        [out:json];
        (
            node["railway"="station"]["network"="KAI Commuter"](around:50000,-6.2088,106.8456);
        );
        out body;
        ";
        response = requests.get(overpass_url, params={'data': query})
        if response.status_code == 200:
            data = response.json()
            stations = []
            for element in data["elements"]:
                if element["type"] == "node" and "tags" in element:
                    stations.append({
                        "lat": element["lat"],
                        "lon": element["lon"],
                        "name": element["tags"].get("name", "Unknown Station")
                    })
            return stations
        return []

    def find_nearest_station(user_lat, user_lon, stations):
        if not stations:
            return None, None
        nearest_station = min(stations, key=lambda s: geodesic((user_lat, user_lon), (s["lat"], s["lon"])).meters)
        distance = geodesic((user_lat, user_lon), (nearest_station["lat"], nearest_station["lon"])).meters
        return nearest_station, distance

    @st.cache_data
    def get_railway_tracks():
        overpass_url = "http://overpass-api.de/api/interpreter"
        query = """
        [out:json];
        (
            way["railway"="rail"](around:50000,-6.2088,106.8456);
            node(w);
        );
        out body;
        ";
        response = requests.get(overpass_url, params={'data': query})
        if response.status_code == 200:
            data = response.json()
            nodes = {element["id"]: (element["lon"], element["lat"]) for element in data["elements"] if element["type"] == "node"}
            tracks = []

            for element in data["elements"]:
                if element["type"] == "way" and "nodes" in element:
                    track_coords = [[nodes[node_id][0], nodes[node_id][1]] for node_id in element["nodes"] if node_id in nodes]
                    if track_coords:
                        tracks.append({"path": track_coords})
            
            return tracks
        return []
    
    user_layer = pdk.Layer("ScatterplotLayer", [{"lat": lat, "lon": lon}], get_position="[lon, lat]", get_color="[0, 0, 255, 255]", get_radius=150)
    
    if option == "KRL Tracker":
        stations = get_krl_data()
        railway_tracks = get_railway_tracks()
    
        nearest_station, distance = find_nearest_station(lat, lon, stations)
        if nearest_station:
            st.info(f"Nearest Station: {nearest_station['name']} ({distance:.2f} meters away)")
        
        station_layer = pdk.Layer("ScatterplotLayer", stations, get_position="[lon, lat]", get_color="[255, 0, 0, 255]", get_radius=120)
        
        station_text_layer = pdk.Layer(
            "TextLayer",
            stations,
            get_position="[lon, lat]",
            get_text="name",
            get_size=18,
            get_color=[255, 255, 255],
            get_angle=0,
            anchor="middle",
            alignment_baseline="bottom"
        )
        
        railway_layer = pdk.Layer("PathLayer", railway_tracks, get_path="path", get_color="[100, 100, 100, 160]", width_scale=20, width_min_pixels=2)
    
    view_state = pdk.ViewState(latitude=lat, longitude=lon, zoom=13)
    layers = [user_layer]
    
    if option == "KRL Tracker":
        layers.extend([railway_layer, station_layer, station_text_layer])
    
    st.pydeck_chart(pdk.Deck(layers=layers, initial_view_state=view_state, map_style="mapbox://styles/mapbox/outdoors-v11"))
else:
    st.warning("Waiting for GPS location... Please allow location access.")

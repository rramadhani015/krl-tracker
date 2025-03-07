import streamlit as st
import requests
import pydeck as pdk
from streamlit_js_eval import get_geolocation
from geopy.distance import geodesic

st.title("📍 KRL Commuterline Tracker")

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
        >;
        out skel qt;
        """
        response = requests.get(overpass_url, params={'data': query})
        if response.status_code == 200:
            data = response.json()
            stations = []

            # Extract stations
            for element in data["elements"]:
                if element["type"] == "node" and "tags" in element:
                    stations.append({
                        "lat": element["lat"],
                        "lon": element["lon"],
                        "name": element["tags"].get("name", "Unknown Station")
                    })
            return stations
        return []

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
        """
        response = requests.get(overpass_url, params={'data': query})
        if response.status_code == 200:
            data = response.json()
            nodes = {element["id"]: (element["lon"], element["lat"]) for element in data["elements"] if element["type"] == "node"}
            tracks = []

            for element in data["elements"]:
                if element["type"] == "way" and "nodes" in element:
                    track_coords = [[nodes[node_id][0], nodes[node_id][1]] for node_id in element["nodes"] if node_id in nodes]
                    if track_coords:
                        tracks.append({"path": track_coords})  # Ensure path is properly formatted
            
            return tracks
        return []

    stations = get_krl_data()
    railway_tracks = get_railway_tracks()

    if stations:
        def find_nearest_stations(lat, lon, stations):
            sorted_stations = sorted(stations, key=lambda s: geodesic((lat, lon), (s["lat"], s["lon"])))
            return sorted_stations[:2] if len(sorted_stations) > 1 else sorted_stations

        nearest_stations = find_nearest_stations(lat, lon, stations)

        # Check if user is inside a station (100m buffer)
        inside_station = any(geodesic((lat, lon), (s["lat"], s["lon"])).meters <= 100 for s in stations)
        if inside_station:
            st.success("You are inside a station area!")

        # Create Pydeck layer for stations (placed above railway)
        station_layer = pdk.Layer(
            "ScatterplotLayer",
            data=stations,
            get_position="[lon, lat]",
            get_color="[255, 0, 0, 255]",
            get_radius=120,
            pickable=True,
            tooltip=True
        )

        # Create Pydeck layer for user location
        user_layer = pdk.Layer(
            "ScatterplotLayer",
            data=[{"lat": lat, "lon": lon}],
            get_position="[lon, lat]",
            get_color="[0, 0, 255, 255]",
            get_radius=150,
            pickable=True,
            tooltip=True
        )

        # Create Pydeck layer for railway tracks
        railway_layer = pdk.Layer(
            "PathLayer",
            data=railway_tracks,
            get_path="path",
            get_color="[0, 255, 0, 160]",
            width_scale=20,
            width_min_pixels=2,
        )

        # Create Pydeck map with a different basemap
        view_state = pdk.ViewState(latitude=lat, longitude=lon, zoom=13)
        r = pdk.Deck(
            layers=[railway_layer, station_layer, user_layer],  # Ensure railway is drawn first
            initial_view_state=view_state,
            map_style="mapbox://styles/mapbox/outdoors-v11"  # Change basemap here
        )
        st.pydeck_chart(r)

        # Show nearest stations
        if len(nearest_stations) == 2:
            st.success(f"You are between **{nearest_stations[0]['name']}** and **{nearest_stations[1]['name']}**.")
        else:
            st.info(f"Nearest Station: **{nearest_stations[0]['name']}**.")
    else:
        st.error("No KRL stations found.")
else:
    st.warning("Waiting for GPS location... Please allow location access.")

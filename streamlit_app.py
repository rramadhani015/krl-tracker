import streamlit as st
import requests
import folium
from streamlit_folium import folium_static
from geopy.distance import geodesic

def get_location():
    js_code = """
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const { latitude, longitude } = position.coords;
            document.getElementById("location").value = `${latitude},${longitude}`;
        },
        (error) => { console.error(error); }
    );
    """
    location = st.text_input("GPS Location", key="location")
    st.write("If location doesn't update, allow location access in your browser settings.")

    st.components.v1.html(f'<script>{js_code}</script><input type="hidden" id="location">', height=0)

    if location:
        lat, lon = map(float, location.split(","))
        return lat, lon
    return None

def get_krl_stations():
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = """
    [out:json];
        node["railway"="station"](around:50000,-6.2088,106.8456);
    out body;
    """
    response = requests.get(overpass_url, params={'data': query})
    
    if response.status_code == 200:
        data = response.json()
        stations = [(node["lat"], node["lon"], node["tags"].get("name", "Unknown Station")) for node in data.get("elements", [])]
        return stations
    return []

def find_nearest_stations(lat, lon, stations):
    sorted_stations = sorted(stations, key=lambda station: geodesic((lat, lon), (station[0], station[1])).meters)
    return sorted_stations[:2] if len(sorted_stations) > 1 else sorted_stations

st.title("📍 KRL Commuterline Tracker")

location = get_location()
if location:
    st.success(f"Your current location: {location}")
    stations = get_krl_stations()
    
    if stations:
        nearest_stations = find_nearest_stations(*location, stations)
        
        # Initialize map
        m = folium.Map(location=location, zoom_start=13)
        folium.Marker(location, tooltip="You Are Here", icon=folium.Icon(color="blue")).add_to(m)
        
        for station in stations:
            folium.Marker([station[0], station[1]], tooltip=station[2], icon=folium.Icon(color="red")).add_to(m)
        
        if len(nearest_stations) == 2:
            station1, station2 = nearest_stations
            st.success(f"You are between {station1[2]} and {station2[2]}.")
            st.write(f"📍 {station1[2]}: ({station1[0]}, {station1[1]})")
            st.write(f"📍 {station2[2]}: ({station2[0]}, {station2[1]})")
        else:
            st.info(f"Nearest Station: {nearest_stations[0][2]} at ({nearest_stations[0][0]}, {nearest_stations[0][1]})")
        
        # Show map
        folium_static(m)
    else:
        st.error("No KRL stations found in Jakarta dataset.")
else:
    st.warning("Waiting for GPS location... Please allow location access.")


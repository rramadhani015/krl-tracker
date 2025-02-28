import geocoder
import requests
import streamlit as st
import folium
from streamlit_folium import folium_static

# Function to get user's location
def get_location():
    g = geocoder.ip('me')  # Get approximate location from IP
    if g.latlng:
        return g.latlng  # Returns (latitude, longitude)
    else:
        return None

# Function to get KRL stations from Overpass API
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
        stations = [(node["lat"], node["lon"], node["tags"].get("name", "Unknown Station")) for node in data.get("elements", [])]
        return stations
    return []

# Streamlit UI
st.title("📍 KRL Commuterline Tracker")

location = get_location()
if location:
    st.write(f"Your current location: {location}")
    stations = get_krl_stations()
    if stations:
        # Initialize map
        m = folium.Map(location=location, zoom_start=13)
        folium.Marker(location, tooltip="You Are Here", icon=folium.Icon(color="blue")).add_to(m)
        
        for station in stations:
            folium.Marker([station[0], station[1]], tooltip=station[2], icon=folium.Icon(color="red")).add_to(m)
        
        # Show map
        folium_static(m)
    else:
        st.error("No KRL stations found in Jakarta dataset.")
else:
    st.error("Could not determine your location.")

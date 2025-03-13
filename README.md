# KRL Public Transport Tracker

## Overview
KRL Public Transport Tracker is a Streamlit-based application that helps users track their location in real-time and find the nearest KRL Commuter station. It also visualizes railway tracks and station locations using OpenStreetMap (OSM) data and PyDeck for interactive mapping.

## Features
- Real-time GPS location tracking
- Identification of the nearest KRL station
- Visualization of KRL stations and railway tracks
- Interactive map using PyDeck
- Uses OpenStreetMap Overpass API for fetching station and railway data

## Installation
To run this application, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/krl-tracker.git
   cd krl-tracker
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the application:
   ```sh
   streamlit run app.py
   ```

## Dependencies
This project requires the following Python libraries:
- `streamlit`
- `requests`
- `pydeck`
- `streamlit_js_eval`
- `geopy`

Install them using:
```sh
pip install streamlit requests pydeck streamlit_js_eval geopy
```

## How It Works
1. The app fetches real-time GPS location data using `streamlit_js_eval`.
2. It queries OpenStreetMap Overpass API to retrieve station and railway track data.
3. The nearest station is calculated using the `geopy` library.
4. PyDeck is used to visualize:
   - User's current location
   - Nearby KRL stations with tooltips showing station names
   - Railway tracks
5. The map is interactive, allowing users to explore the railway network.

## Usage
- Open the app and allow location access.
- View your current location and the nearest station.
- Hover over stations to see their names.
- Explore railway tracks and station locations on the interactive map.

## License
This project is open-source and licensed under the MIT License.

## Contribution
Feel free to contribute by submitting issues or pull requests to improve the app.

## Acknowledgments
- OpenStreetMap for station and railway data
- PyDeck for map visualization
- Streamlit for the interactive interface


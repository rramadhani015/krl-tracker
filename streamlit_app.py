import numpy as np
import matplotlib.pyplot as plt
import rasterio
import pydeck as pdk
from rasterio.plot import show
from io import BytesIO
import requests
from PIL import Image

# Define the URL for AWS Terrarium DEM (Example: Indonesia Region)
TERRAIN_URL = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"

# Define the color ramp using Matplotlib colormap
COLORMAP = plt.get_cmap("terrain")  # You can also try "viridis", "plasma", etc.

def fetch_terrain_tile(z, x, y):
    """Fetches a terrain RGB tile from AWS Terrarium."""
    url = TERRAIN_URL.format(z=z, x=x, y=y)
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        print("Failed to fetch terrain tile")
        return None

def convert_rgb_to_elevation(img):
    """Converts a terrain RGB image to elevation values."""
    img = np.array(img, dtype=np.float32)  # Ensure correct dtype
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    elevation = (r * 256 + g + b / 256) - 32768
    return elevation

def apply_colormap(elevation):
    """Applies a colormap to the elevation data."""
    norm_elevation = (elevation - np.min(elevation)) / (np.max(elevation) - np.min(elevation))
    colored = COLORMAP(norm_elevation)
    return (colored[:, :, :3] * 255).astype(np.uint8)  # Convert to 8-bit RGB

# Fetch and process a tile
z, x, y = 6, 55, 32  # Example tile coordinates
terrain_tile = fetch_terrain_tile(z, x, y)
if terrain_tile:
    elevation = convert_rgb_to_elevation(terrain_tile)
    colored_tile = apply_colormap(elevation)
    colored_image = Image.fromarray(colored_tile)
    
    # Save the image or visualize it
    colored_image.save("colored_terrain.png")
    plt.imshow(colored_tile)
    plt.axis("off")
    plt.show()
    
    # Pydeck visualization
    view = pdk.ViewState(latitude=-2.5, longitude=117.5, zoom=4, pitch=60)
    
    layer = pdk.Layer(
        "BitmapLayer",
        data=None,
        image="colored_terrain.png",  # Load pre-colored terrain texture
        bounds=[113, -5, 122, 0],  # Example bounding box for Indonesia
    )
    
    deck = pdk.Deck(layers=[layer], initial_view_state=view)
    deck.to_html("terrain_colormap.html")  # Export as interactive HTML

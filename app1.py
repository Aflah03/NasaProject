import requests
import rasterio
import matplotlib.pyplot as plt
from rasterio.plot import show

# URL for today.tif (nowcast data)
url = 'https://maps.nccs.nasa.gov/download/landslides/latest/today.tif'

# Function to download the file
def download_file(url, filename):
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                if chunk:  # Filter out keep-alive new chunks
                    f.write(chunk)
        print(f"Successfully downloaded {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {filename}: {e}")

# Function to visualize the TIFF file
def visualize_tiff(filename):
    try:
        with rasterio.open(filename) as src:
            fig, ax = plt.subplots(figsize=(10, 10))
            show(src, ax=ax, cmap='viridis')
            ax.set_title('TIFF Visualization')
            plt.colorbar(ax.images[0], ax=ax, orientation='vertical', label='Pixel Values')
            plt.show()
        print(f"Successfully visualized {filename}")
    except Exception as e:
        print(f"Failed to visualize {filename}: {e}")

# Download and visualize the TIFF file
filename = 'today.tif'
download_file(url, filename)
visualize_tiff(filename)

import requests
import rasterio
import matplotlib.pyplot as plt
from shapely.geometry import box
from rasterio.mask import mask

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
        print(f"Failed to download {filename}. Error: {str(e)}")

# Function to visualize the .tif file for a specific area
def visualize_tif_for_area(filename, bbox):
    with rasterio.open(filename) as src:
        # Define the bounding box for Kerala (more accurate coordinates)
        kerala_bbox = box(*bbox)
        # Clip the raster to the bounding box
        out_image, out_transform = mask(src, [kerala_bbox], crop=True)
        out_image = out_image[0]  # Get the first band

        plt.imshow(out_image, cmap='gray')
        plt.colorbar()
        plt.title(f"Visualization of {filename} for Kerala")
        plt.show()

# Download the file
download_file(url, 'today.tif')

# Define the bounding box for Kerala (more accurate coordinates)
kerala_bbox = [74.85, 8.07, 77.57, 12.77]  # [min_lon, min_lat, max_lon, max_lat]

# Visualize the downloaded .tif file for Kerala
visualize_tif_for_area('today.tif', kerala_bbox)

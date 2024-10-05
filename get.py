import requests
import rasterio
from shapely.geometry import box
from rasterio.mask import mask
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.colorbar import ColorbarBase
import json

url = 'https://maps.nccs.nasa.gov/download/landslides/latest/today.tif'

def download_file(url, filename):
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status() 
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                if chunk:  
                    f.write(chunk)
        print(f"Successfully downloaded {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {filename}. Error: {str(e)}")

def parse_tif_and_save_as_png(filename, bbox, output_image, output_colorbar, output_json):
    with rasterio.open(filename) as src:
        kerala_bbox = box(*bbox)
        out_image, out_transform = mask(src, [kerala_bbox], crop=True)
        out_image = out_image[0]  # Get the first band

        # Normalize the data for better visualization
        out_image = out_image.astype(float)  # Convert to float for normalization
        out_image[out_image == 0] = np.nan  # Set no data values to NaN
        norm_data = (out_image - np.nanmin(out_image)) / (np.nanmax(out_image) - np.nanmin(out_image))  # Normalize to [0, 1]

        # Save the normalized data as a PNG image with a more intense color map
        plt.imsave(output_image, norm_data, cmap='inferno')

        # Create a color bar
        fig, ax = plt.subplots(figsize=(6, 1))
        fig.subplots_adjust(bottom=0.5)

        norm = Normalize(vmin=np.nanmin(out_image), vmax=np.nanmax(out_image))
        cb = ColorbarBase(ax, cmap='inferno', norm=norm, orientation='horizontal')
        cb.set_label('Landslide Forecast Intensity')

        # Save the color bar as a PNG image
        plt.savefig(output_colorbar, bbox_inches='tight')

        # Identify high-risk areas (e.g., normalized value > 0.8)
        high_risk_indices = np.where(norm_data > 0.8)
        high_risk_coords = []
        for y, x in zip(*high_risk_indices):
            lon, lat = out_transform * (x, y)
            high_risk_coords.append([lat, lon])

        # Save high-risk coordinates to a JSON file
        with open(output_json, 'w') as json_file:
            json.dump(high_risk_coords, json_file)

# Download the file
download_file(url, 'today.tif')

# Define the bounding box for Kerala (more accurate coordinates)
kerala_bbox = [74.85, 8.07, 77.57, 12.77]  # [min_lon, min_lat, max_lon, max_lat]

# Parse the .tif file and save as PNG and JSON
parse_tif_and_save_as_png('today.tif', kerala_bbox, 'kerala_landslide_forecast.png', 'colorbar.png', 'high_risk_areas.json')
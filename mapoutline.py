import requests
import rasterio
import matplotlib.pyplot as plt
from shapely.geometry import box
from rasterio.mask import mask

# Function to download the LHASA landslide forecast file
def download_lhasa_file(url, filename):
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

# URL for LHASA landslide forecast data
lhasa_url = 'https://maps.nccs.nasa.gov/download/landslides/latest/today.tif'
download_lhasa_file(lhasa_url, 'today.tif')

# Load SRTM data and LHASA data
srtm_filename = 'srtm_data.tif'  # Replace with your downloaded SRTM filename
lhasa_filename = 'today.tif'

# Define the bounding box for Kerala
kerala_bbox = [74.85, 8.07, 77.57, 12.77]  # [min_lon, min_lat, max_lon, max_lat]

# Function to visualize both datasets
def visualize_combined_data(srtm_filename, lhasa_filename, bbox):
    with rasterio.open(srtm_filename) as srtm_src:
        with rasterio.open(lhasa_filename) as lhasa_src:
            # Define the bounding box for Kerala
            kerala_box = box(*bbox)
           
            # Mask and crop SRTM data
            srtm_out_image, srtm_out_transform = mask(srtm_src, [kerala_box], crop=True)
            srtm_out_image = srtm_out_image[0]  # Get the first band

            # Mask and crop LHASA data
            lhasa_out_image, lhasa_out_transform = mask(lhasa_src, [kerala_box], crop=True)
            lhasa_out_image = lhasa_out_image[0]  # Get the first band

            # Set up the plot
            fig, ax = plt.subplots(1, 2, figsize=(15, 7))

            # Visualize SRTM data
            ax[0].imshow(srtm_out_image, cmap='terrain')
            ax[0].set_title('SRTM Elevation Data for Kerala')
            ax[0].set_xlabel('Longitude')
            ax[0].set_ylabel('Latitude')
            plt.colorbar(ax[0].images[0], ax=ax[0], label='Elevation (meters)')

            # Visualize LHASA data
            ax[1].imshow(lhasa_out_image, cmap='hot', alpha=0.5)
            ax[1].set_title('LHASA Landslide Forecast Data for Kerala')
            ax[1].set_xlabel('Longitude')
            ax[1].set_ylabel('Latitude')
            plt.colorbar(ax[1].images[0], ax=ax[1], label='Landslide Probability')

            plt.tight_layout()
            plt.show()

# Visualize both datasets
visualize_combined_data(srtm_filename, lhasa_filename, kerala_bbox)
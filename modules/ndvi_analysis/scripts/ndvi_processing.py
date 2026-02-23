import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import cv2
from matplotlib import colors



# 1. Carregamento do Raster


def load_multiband_raster(filepath):
    """
    Load multiband raster and return array.
    """
    with rasterio.open(filepath) as raster:
        return raster.read()



# 2. Calculo do NDVI


def calculate_ndvi(band_red, band_nir):
    """
    Calculate NDVI using RED and NIR bands.
    NDVI = (NIR - RED) / (NIR + RED)
    """
    np.seterr(divide='ignore', invalid='ignore')
    return (band_nir.astype(float) - band_red.astype(float)) / \
           (band_nir + band_red)



# 3. Plot NDVI


class MidpointNormalize(colors.Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        super().__init__(vmin, vmax, clip)

    def __call__(self, value, clip=None):
        x = [self.vmin, self.midpoint, self.vmax]
        y = [0, 0.5, 1]
        return np.ma.masked_array(
            np.interp(value, x, y),
            np.isnan(value)
        )


def plot_ndvi(ndvi):
    min_val = np.nanmin(ndvi)
    max_val = np.nanmax(ndvi)
    mid = 0.1

    colormap = plt.cm.RdYlGn
    norm = MidpointNormalize(vmin=min_val, vmax=max_val, midpoint=mid)

    fig, ax = plt.subplots(figsize=(16, 8))
    cbar_plot = ax.imshow(ndvi, cmap=colormap, vmin=min_val, vmax=max_val)

    ax.axis('off')
    ax.set_title("NDVI - Fort Lauderdale - 06/03/2023")

    fig.colorbar(cbar_plot, orientation='horizontal', shrink=0.65)
    fig.savefig("outputs/ndvi_fort_lauderdale.png", dpi=300, bbox_inches='tight')
    plt.show()



# 4. Histograma


def plot_histogram(ndvi):
    fig, ax = plt.subplots(figsize=(12, 6))

    x = ndvi[~np.isnan(ndvi)]
    ax.hist(x, bins=30, color='green', ec='black')

    ax.set_title("NDVI Histograma - Fort Lauderdale - 06/03/2023")
    ax.set_xlabel("NDVI valores")
    ax.set_ylabel("Número de pixels")

    fig.savefig("outputs/histograma_fort_lauderdale.png", dpi=300, bbox_inches='tight')

    plt.show()



# 5. Classificação


def classify_ndvi(ndvi):
    bins = [-1, -0.5, 0, 0.25, 0.5, 1]
    classified = np.digitize(ndvi, bins)
    return classified.astype(np.uint8)

def plot_classification(classified):
    cmap = colors.ListedColormap(
        ['white', 'red', 'orange', 'yellow', 'green', 'darkgreen']
    )

    fig, ax = plt.subplots(figsize=(14, 8))
    im = ax.imshow(classified, cmap=cmap, vmin=1, vmax=6)

    ax.axis('off')
    ax.set_title("NDVI Classificação - Fort Lauderdale - 06/03/2023")

    fig.savefig("outputs/ndvi_classificado.png",
                dpi=300, bbox_inches='tight')

    plt.show()

def apply_median_filter(classified):
    return cv2.medianBlur(classified, 13)

def plot_median_filtered(median_filtered):
    cmap = colors.ListedColormap(
        ['white', 'red', 'orange', 'yellow', 'green', 'darkgreen']
    )

    fig, ax = plt.subplots(figsize=(14, 8))
    im = ax.imshow(median_filtered, cmap=cmap, vmin=1, vmax=6)

    ax.axis('off')
    ax.set_title("NDVI Filtro Mediano - Fort Lauderdale - 06/03/2023")

    fig.savefig("outputs/ndvi_filtro_mediano.png",
                dpi=300, bbox_inches='tight')

    plt.show()

def smooth_classification(classified):
    return cv2.medianBlur(classified, 13)



# 6. Pipeline Principal


def main():
    filepath = "data/Fort_Lauderdale_MSI_all_bands.tif"

    raster_arr = load_multiband_raster(filepath)

    band_red = raster_arr[3]   # B4
    band_nir = raster_arr[7]   # B8

    ndvi = calculate_ndvi(band_red, band_nir)

    print("NDVI Min:", np.nanmin(ndvi))
    print("NDVI Max:", np.nanmax(ndvi))

    plot_ndvi(ndvi)
    plot_histogram(ndvi)

    classified = classify_ndvi(ndvi)
    plot_classification(classified)           

    smoothed = smooth_classification(classified)
    plot_median_filtered(smoothed)            


if __name__ == "__main__":
    main()
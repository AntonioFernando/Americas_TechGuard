import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import cv2
from matplotlib import colors


# 1. Load Raster

def load_multiband_raster(filepath):
    """
    Load multiband raster and return array.
    """
    with rasterio.open(filepath) as raster:
        return raster.read()


# 2. Calculate NDVI

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


def plot_ndvi(ndvi, output_dir):
    min_val = np.nanmin(ndvi)
    max_val = np.nanmax(ndvi)
    mid = 0.1

    colormap = plt.cm.RdYlGn
    norm = MidpointNormalize(vmin=min_val, vmax=max_val, midpoint=mid)

    fig, ax = plt.subplots(figsize=(16, 8))
    cbar_plot = ax.imshow(ndvi, cmap=colormap, norm=norm)

    ax.axis('off')
    ax.set_title("NDVI - Recife - August 2022")

    fig.colorbar(cbar_plot, orientation='horizontal', shrink=0.65)

    fig.savefig(os.path.join(output_dir, "ndvi_Recife - August 2022.png"),
                dpi=300, bbox_inches='tight')

    plt.show()


# 4. Plots Histogram

def plot_histogram(ndvi, output_dir):
    fig, ax = plt.subplots(figsize=(12, 6))

    x = ndvi[~np.isnan(ndvi)]
    ax.hist(x, bins=30, color='green', ec='black')

    ax.set_title("NDVI Histogram - Recife - August 2022")
    ax.set_xlabel("NDVI values")
    ax.set_ylabel("Pixels number")

    fig.savefig(os.path.join(output_dir, "histogram_Recife.png"),
                dpi=300, bbox_inches='tight')

    plt.show()


# 5. Plots Classification

def classify_ndvi(ndvi):
    bins = [-1, -0.5, 0, 0.25, 0.5, 1]
    classified = np.digitize(ndvi, bins)
    return classified.astype(np.uint8)


def plot_classification(classified, output_dir):
    cmap = colors.ListedColormap(
        ['white', 'red', 'orange', 'yellow', 'green', 'darkgreen']
    )

    fig, ax = plt.subplots(figsize=(14, 8))
    ax.imshow(classified, cmap=cmap, vmin=1, vmax=6)

    ax.axis('off')
    ax.set_title("NDVI Classification - Recife - August 2022")

    fig.savefig(os.path.join(output_dir, "ndvi_classified.png"),
                dpi=300, bbox_inches='tight')

    plt.show()


# 6. Plots Median

def smooth_classification(classified):
    return cv2.medianBlur(classified, 13)


def plot_median_filtered(median_filtered, output_dir):
    cmap = colors.ListedColormap(
        ['white', 'red', 'orange', 'yellow', 'green', 'darkgreen']
    )

    fig, ax = plt.subplots(figsize=(14, 8))
    ax.imshow(median_filtered, cmap=cmap, vmin=1, vmax=6)

    ax.axis('off')
    ax.set_title("NDVI Median filter - Recife - August 2022")

    fig.savefig(os.path.join(output_dir, "ndvi_median_filter.png"),
                dpi=300, bbox_inches='tight')

    plt.show()


# 7. Main Pipeline

def main():

    # Diretório base do script (modules/ndvi_analysis/scripts)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Volta até a raiz do projeto (Americas_Techguard)
    project_root = os.path.abspath(
        os.path.join(base_dir, "..", "..", "..")
    )

    # Caminho da pasta data (na raiz)
    data_dir = os.path.join(project_root, "data")

    # Caminho da pasta outputs (dentro do módulo ndvi_analysis)
    output_dir = os.path.abspath(
        os.path.join(base_dir, "..", "outputs")
    )

    # Garante que a pasta outputs exista
    os.makedirs(output_dir, exist_ok=True)

    # Caminho completo do arquivo raster
    filepath = os.path.join(data_dir, "Recife_MSI_all_bands_20_august_2022.tif")

    # Verifica se o arquivo existe
    if not os.path.exists(filepath):
        print(f"Error: File not found {filepath}")
        return

    # Carrega raster
    raster_arr = load_multiband_raster(filepath)

    band_red = raster_arr[3]   # B4
    band_nir = raster_arr[7]   # B8

    ndvi = calculate_ndvi(band_red, band_nir)

    print("NDVI Min:", np.nanmin(ndvi))
    print("NDVI Max:", np.nanmax(ndvi))

    plot_ndvi(ndvi, output_dir)
    plot_histogram(ndvi, output_dir)

    classified = classify_ndvi(ndvi)
    plot_classification(classified, output_dir)

    smoothed = smooth_classification(classified)
    plot_median_filtered(smoothed, output_dir)


if __name__ == "__main__":
    main()
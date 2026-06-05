import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
from matplotlib import colors

from ndvi_processing import load_multiband_raster, calculate_ndvi

# Funções básicas

class MidpointNormalize(colors.Normalize):
    """Normalização para colormap com midpoint"""
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        super().__init__(vmin, vmax, clip)

    def __call__(self, value, clip=None):
        x = [self.vmin, self.midpoint, self.vmax]
        y = [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y), np.isnan(value))

def plot_ndvi(ndvi, title, filename, output_dir, midpoint=0.1):
    """Plota NDVI ou ΔNDVI"""
    min_val, max_val = np.nanmin(ndvi), np.nanmax(ndvi)
    norm = MidpointNormalize(vmin=min_val, vmax=max_val, midpoint=midpoint)
    fig, ax = plt.subplots(figsize=(14, 7))
    im = ax.imshow(ndvi, cmap=plt.cm.RdYlGn, norm=norm)
    ax.axis('off')
    ax.set_title(title)
    fig.colorbar(im, orientation='horizontal', shrink=0.65)
    fig.savefig(os.path.join(output_dir, filename), dpi=300, bbox_inches='tight')
    plt.show()

def plot_histogram(ndvi, title, filename, output_dir):
    """Plota histograma do NDVI"""
    fig, ax = plt.subplots(figsize=(10, 5))
    x = ndvi[~np.isnan(ndvi)]
    ax.hist(x, bins=30, color='green', ec='black')
    ax.set_title(title)
    ax.set_xlabel("NDVI valores")
    ax.set_ylabel("Número de pixels")
    fig.savefig(os.path.join(output_dir, filename), dpi=300, bbox_inches='tight')
    plt.show()

def classify_ndvi(ndvi, bins):
    """Classifica NDVI em bins"""
    classified = np.digitize(ndvi, bins)
    return classified.astype(np.uint8)

def smooth_classification(classified, ksize=13):
    """Aplica filtro mediano"""
    return cv2.medianBlur(classified, ksize)


# Pipeline Principal

def main():
    # Diretórios
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, "..", "..", ".."))
    data_dir = os.path.join(project_root, "data")
    output_dir = os.path.join(base_dir, "..", "outputs")
    os.makedirs(output_dir, exist_ok=True)

    # Arquivos raster
    filepath_1 = os.path.join(data_dir, "Recife_MSI_all_bands_2_abril_2022.tif")
    filepath_2 = os.path.join(data_dir, "Recife_MSI_all_bands_20_agosto_2022.tif")
    for fp in [filepath_1, filepath_2]:
        if not os.path.exists(fp):
            print(f"Erro: arquivo não encontrado em {fp}")
            return

    # Carrega rasters
    raster_1 = load_multiband_raster(filepath_1)
    raster_2 = load_multiband_raster(filepath_2)

    # Seleciona bandas RED e NIR
    red_1, nir_1 = raster_1[3], raster_1[7]
    red_2, nir_2 = raster_2[3], raster_2[7]

    # Calcula NDVI
    ndvi_1 = calculate_ndvi(red_1, nir_1)
    ndvi_2 = calculate_ndvi(red_2, nir_2)
    delta_ndvi = ndvi_2 - ndvi_1

   
    # Plots NDVI
   
    plot_ndvi(ndvi_1, "NDVI - REcife - April 2022", "ndvi_march.png", output_dir)
    plot_ndvi(ndvi_2, "NDVI - Recife - August 2022", "ndvi_october.png", output_dir)
    plot_ndvi(delta_ndvi, "ΔNDVI (August - April)", "delta_ndvi.png", output_dir, midpoint=0)

   
    # Histogramas
    
    plot_histogram(ndvi_1, "Histogram NDVI - March", "hist_ndvi_march.png", output_dir)
    plot_histogram(ndvi_2, "Histogram NDVI - October", "hist_ndvi_october.png", output_dir)
    plot_histogram(delta_ndvi, "Histogram ΔNDVI", "hist_delta_ndvi.png", output_dir)

   
    
    # Classificação e filtro mediano do ΔNDVI
    

    # Calcula bins automaticamente com base nos valores do delta
    delta_min, delta_max = np.nanmin(delta_ndvi), np.nanmax(delta_ndvi)
    bins = np.linspace(delta_min, delta_max, 6)  # 5 classes uniformes

    classified = classify_ndvi(delta_ndvi, bins)
    smoothed = smooth_classification(classified)

    # Ajusta o midpoint para o centro do delta real
    mid_val = (delta_min + delta_max) / 2

    # Informações rápidas
    print("NDVI March Min/Max:", np.nanmin(ndvi_1), np.nanmax(ndvi_1))
    print("NDVI October Min/Max:", np.nanmin(ndvi_2), np.nanmax(ndvi_2))
    print("ΔNDVI Min/Max:", np.nanmin(delta_ndvi), np.nanmax(delta_ndvi))

if __name__ == "__main__":
    main()
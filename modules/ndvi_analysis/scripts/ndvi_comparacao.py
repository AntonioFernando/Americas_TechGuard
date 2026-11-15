import os
import numpy as np
import rasterio
import matplotlib.pyplot as plt

from ndvi_processing import load_multiband_raster, calculate_ndvi
from ndvi_metricas import descriptive_statistics, area_by_class

def process_ndvi(filepath):
    """Carrega o raster, calcula NDVI, estatísticas e área por classe"""
    raster_arr = load_multiband_raster(filepath)

    band_red = raster_arr[3]
    band_nir = raster_arr[7]

    ndvi = calculate_ndvi(band_red, band_nir)

    with rasterio.open(filepath) as src:
        transform = src.transform
        pixel_area = transform[0] * abs(transform[4])

    stats = descriptive_statistics(ndvi)
    areas = area_by_class(ndvi, pixel_area)

    return ndvi, stats, areas

def calculate_difference(ndvi1, ndvi2):
    """Calcula a diferença NDVI entre duas imagens"""
    return ndvi2 - ndvi1

def plot_comparison(areas_marco, areas_outubro, output_dir):
    """Plota gráfico comparando porcentagem de classes e salva em output_dir"""
    classes = list(areas_marco.keys())

    perc_marco = [areas_marco[c]["porcentagem"] for c in classes]
    perc_out = [areas_outubro[c]["porcentagem"] for c in classes]

    x = np.arange(len(classes))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10,6))

    ax.bar(x - width/2, perc_marco, width, label="March")
    ax.bar(x + width/2, perc_out, width, label="October")

    ax.set_xticks(x)
    ax.set_xticklabels(classes, rotation=45)
    ax.set_ylabel("Percentage (%)")
    ax.set_title("Comparation NDVI - March vs October")
    ax.legend()

    # Salvar gráfico no diretório outputs
    fig.savefig(
        os.path.join(output_dir, "Comparation_march_october_Fort_Lauderdale.png"),
        dpi=300,
        bbox_inches='tight'
    )

    plt.tight_layout()
    plt.show()

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    project_root = os.path.abspath(
        os.path.join(base_dir, "..", "..", "..")
    )

    data_dir = os.path.join(project_root, "data")

    # Definir caminhos das imagens
    filepath_marco = os.path.join(data_dir, "Fort_Lauderdale_MSI_all_bands.tif")
    filepath_outubro = os.path.join(data_dir, "Fort_Lauderdale_MSI_all_bands_after_flood_april_15th.tif")

    # Processar NDVI
    ndvi_marco, stats_marco, areas_marco = process_ndvi(filepath_marco)
    ndvi_out, stats_out, areas_out = process_ndvi(filepath_outubro)

    # Mostrar estatísticas
    print("\n=== Statistics March ===")
    for k, v in stats_marco.items():
        print(f"{k}: {v:.4f}")

    print("\n=== Statistics October ===")
    for k, v in stats_out.items():
        print(f"{k}: {v:.4f}")

    # Criar diretório de saída
    output_dir = os.path.join(project_root, "modules", "ndvi_analysis", "outputs")
    os.makedirs(output_dir, exist_ok=True)

    # Comparação das áreas por classe
    plot_comparison(areas_marco, areas_out, output_dir)

    # Diferença NDVI
    ndvi_diff = calculate_difference(ndvi_marco, ndvi_out)

    # Mostrar e salvar mapa da diferença NDVI
    plt.figure(figsize=(10,8))
    im = plt.imshow(ndvi_diff, cmap="RdYlGn")
    plt.colorbar(im, label="NDVI difference (October - March)")
    plt.title("Difference NDVI October - March")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "Difference_NDVI_October_March.png"), dpi=300)
    plt.show()

if __name__ == "__main__":
    main()
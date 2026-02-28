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

    ax.bar(x - width/2, perc_marco, width, label="Março")
    ax.bar(x + width/2, perc_out, width, label="Outubro")

    ax.set_xticks(x)
    ax.set_xticklabels(classes, rotation=45)
    ax.set_ylabel("Porcentagem (%)")
    ax.set_title("Comparação NDVI - Março vs Outubro")
    ax.legend()

    # Salvar gráfico no diretório outputs
    fig.savefig(
        os.path.join(output_dir, "Comparacao_marco_outubro_Fort_Lauderdale.png"),
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
    filepath_outubro = os.path.join(data_dir, "Fort_Lauderdale_MSI_all_bands_apos_enchente_outubro.tif")

    # Processar NDVI
    ndvi_marco, stats_marco, areas_marco = process_ndvi(filepath_marco)
    ndvi_out, stats_out, areas_out = process_ndvi(filepath_outubro)

    # Mostrar estatísticas
    print("\n=== ESTATÍSTICAS MARÇO ===")
    for k, v in stats_marco.items():
        print(f"{k}: {v:.4f}")

    print("\n=== ESTATÍSTICAS OUTUBRO ===")
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
    plt.colorbar(im, label="Diferença NDVI (Outubro - Março)")
    plt.title("Diferença NDVI Outubro - Março")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "Diferenca_NDVI_Outubro_Marco.png"), dpi=300)
    plt.show()

if __name__ == "__main__":
    main()
import os
import numpy as np
import matplotlib.pyplot as plt

import rasterio

from ndvi_processing import load_multiband_raster, calculate_ndvi
from ndvi_metricas import descriptive_statistics, area_by_class


def process_ndvi(filepath):

    raster_arr = load_multiband_raster(filepath)

    band_red = raster_arr[3]
    band_nir = raster_arr[7]

    ndvi = calculate_ndvi(band_red, band_nir)

    with rasterio.open(filepath) as src:
        transform = src.transform
        pixel_area = transform[0] * abs(transform[4])

    stats = descriptive_statistics(ndvi)
    areas = area_by_class(ndvi, pixel_area)

    return stats, areas


def compare_statistics(stats1, stats2, label1, label2):

    print(f"\n=== Diferença Estatística ({label1} - {label2}) ===")

    for key in stats1.keys():

        diff = stats1[key] - stats2[key]

        print(f"{key}: {diff:.4f}")


def compare_classes(areas1, areas2, label1, label2):

    print(f"\n=== Diferença Percentual de Classes ({label1} - {label2}) ===")

    for classe in areas1.keys():

        p1 = areas1[classe]["porcentagem"]
        p2 = areas2[classe]["porcentagem"]

        diff = p1 - p2

        print(f"{classe}: {diff:.2f}%")


def plot_class_comparison(areas1, areas2, label1, label2, output_dir):

    classes = list(areas1.keys())

    vals1 = [areas1[c]["porcentagem"] for c in classes]
    vals2 = [areas2[c]["porcentagem"] for c in classes]

    x = np.arange(len(classes))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10,6))

    ax.bar(x - width/2, vals1, width, label=label1)
    ax.bar(x + width/2, vals2, width, label=label2)

    ax.set_ylabel("Percentage (%)")
    ax.set_title("Comparative Analysis of NDVI Classes")
    ax.set_xticks(x)
    ax.set_xticklabels(classes, rotation=45)

    ax.legend()

    plt.tight_layout()

    output_path = os.path.join(output_dir, "comparacao_classes_ndvi.png")
    plt.savefig(output_path, dpi=300)

    plt.show()


def main():

    base_dir = os.path.dirname(os.path.abspath(__file__))

    output_dir = os.path.abspath(
        os.path.join(base_dir, "..", "outputs")
    )
    os.makedirs(output_dir, exist_ok=True)

    project_root = os.path.abspath(
        os.path.join(base_dir, "..", "..", "..")
    )

    data_dir = os.path.join(project_root, "data")

    recife_file = os.path.join(
        data_dir,
        "Recife_MSI_all_bands_20_agosto_2022.tif"
    )

    florida_file = os.path.join(
        data_dir,
        "Fort_Lauderdale_MSI_all_bands_apos_enchente_outubro.tif"
    )

    if not os.path.exists(recife_file):
        print("Arquivo de Recife não encontrado.")
        return

    if not os.path.exists(florida_file):
        print("Arquivo de Fort Lauderdale não encontrado.")
        return

    print("\nProcessando Recife...")
    stats_recife, areas_recife = process_ndvi(recife_file)

    print("\nProcessando Fort Lauderdale...")
    stats_florida, areas_florida = process_ndvi(florida_file)

    print("\n=== Estatísticas Recife ===")
    for k, v in stats_recife.items():
        print(f"{k}: {v:.4f}")

    print("\n=== Estatísticas Fort Lauderdale ===")
    for k, v in stats_florida.items():
        print(f"{k}: {v:.4f}")

    compare_statistics(stats_recife, stats_florida, "Recife", "Fort Lauderdale")

    compare_classes(areas_recife, areas_florida, "Recife", "Fort Lauderdale")

    plot_class_comparison(
        areas_recife,
        areas_florida,
        "Recife",
        "Fort Lauderdale",
        output_dir
    )


if __name__ == "__main__":
    main()
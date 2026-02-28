import os
import numpy as np
import rasterio
import matplotlib.pyplot as plt

from ndvi_processing import load_multiband_raster, calculate_ndvi

def descriptive_statistics(ndvi):

    stats = {
        "mean": np.nanmean(ndvi),
        "median": np.nanmedian(ndvi),
        "std": np.nanstd(ndvi),
        "var": np.nanvar(ndvi),
        "p10": np.nanpercentile(ndvi, 10),
        "p25": np.nanpercentile(ndvi, 25),
        "p75": np.nanpercentile(ndvi, 75),
        "p90": np.nanpercentile(ndvi, 90),
    }

    return stats

def area_by_class(ndvi, pixel_area):

    valid_mask = ~np.isnan(ndvi)
    total_pixels = np.sum(valid_mask)

    classes = {
        "água": ndvi < 0,
        "solo_exposto": (ndvi >= 0) & (ndvi < 0.2),
        "veg_moderada": (ndvi >= 0.2) & (ndvi < 0.5),
        "veg_densa": ndvi >= 0.5
    }

    results = {}

    for name, mask in classes.items():

        pixels = np.sum(mask & valid_mask)
        area_km2 = (pixels * pixel_area) / 1_000_000
        percent = (pixels / total_pixels) * 100

        results[name] = {
            "pixels": pixels,
            "area_km2": area_km2,
            "porcentagem": percent
        }

    return results

def plot_area_distribution(areas, output_dir):

    classes = []
    percentages = []

    for classe, valores in areas.items():
        classes.append(classe)
        percentages.append(valores["porcentagem"])

    fig, ax = plt.subplots(figsize=(10,6))
    ax.bar(classes, percentages)

    ax.set_title("Distribuição Percentual das Classes NDVI — Fort Lauderdale — outubro")
    ax.set_ylabel("Porcentagem (%)")
    ax.set_xlabel("Classes")

    plt.xticks(rotation=45)

    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, "distribuicao_percentual_ndvi.png"), dpi=300)

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

    filepath = os.path.join(
        data_dir,
        "Fort_Lauderdale_MSI_all_bands.tif"
    )

    if not os.path.exists(filepath):
        print("Arquivo não encontrado.")
        return

    # Carregar raster
    raster_arr = load_multiband_raster(filepath)

    band_red = raster_arr[3]
    band_nir = raster_arr[7]

    ndvi = calculate_ndvi(band_red, band_nir)

    # Calcular área do pixel
    with rasterio.open(filepath) as src:
        transform = src.transform
        pixel_area = transform[0] * abs(transform[4])

    stats = descriptive_statistics(ndvi)
    areas = area_by_class(ndvi, pixel_area)

    print("\n=== Estatísticas NDVI ===")
    for k, v in stats.items():
        print(f"{k}: {v:.4f}")

    print("\n=== Área por Classe ===")
    for classe, valores in areas.items():
        print(f"\nClasse: {classe}")
        for metrica, valor in valores.items():
            print(f"{metrica}: {valor:.4f}")

    with rasterio.open(filepath) as src:
        print(src.crs)
        print(src.transform)

    plot_area_distribution(areas, output_dir)

if __name__ == "__main__":
    main()
import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import cv2
from whitebox import WhiteboxTools
from rasterio.warp import reproject, Resampling

# -----------------------------
# Inicializar Whitebox
# -----------------------------
wbt = WhiteboxTools()

# -----------------------------
# Função para tratar NoData
# -----------------------------
def mask_nodata(arr, nodata_value=-9999):
    arr = arr.astype(float)
    arr[arr == nodata_value] = np.nan
    return arr

# -----------------------------
# Normalização robusta
# -----------------------------
def normalize(arr):
    return (arr - np.nanmin(arr)) / (np.nanmax(arr) - np.nanmin(arr) + 1e-8)

# -----------------------------
# Modelo de risco
# -----------------------------
def compute_flood_risk(dem, slope, ndvi=None):

    elev_norm = normalize(dem)
    slope_norm = normalize(slope)

    elev_risk = 1 - elev_norm
    slope_risk = 1 - slope_norm

    if ndvi is not None:
        ndvi_norm = normalize(ndvi)
        ndvi_risk = 1 - ndvi_norm

        flood_risk = (
            0.4 * ndvi_risk +
            0.4 * elev_risk +
            0.2 * slope_risk
        )
    else:
        flood_risk = (
            0.6 * elev_risk +
            0.4 * slope_risk
        )

    return flood_risk

# -----------------------------
# Classificação
# -----------------------------
def classify_risk(flood_risk):

    risk_class = np.zeros_like(flood_risk)

    risk_class[flood_risk < 0.3] = 1
    risk_class[(flood_risk >= 0.3) & (flood_risk < 0.6)] = 2
    risk_class[flood_risk >= 0.6] = 3

    return risk_class.astype(np.uint8)

# -----------------------------
# Suavização (MEDIAN FILTER)
# -----------------------------
def smooth_risk(flood_risk, kernel_size=5):

    if kernel_size % 2 == 0:
        kernel_size += 1

    print(f"Aplicando median filter {kernel_size}x{kernel_size}")

    mask = np.isnan(flood_risk)

    temp = np.nan_to_num(flood_risk, nan=0)

    smoothed = cv2.medianBlur(temp.astype(np.float32), kernel_size)

    smoothed[mask] = np.nan

    return smoothed

# -----------------------------
# MAIN
# -----------------------------
def main():

    base_dir = os.path.dirname(os.path.abspath(__file__))

    project_root = os.path.abspath(
        os.path.join(base_dir, "..", "..", "..")
    )

    data_dir = os.path.join(project_root, "data")

    output_dir = os.path.abspath(
        os.path.join(base_dir, "..", "outputs")
    )

    os.makedirs(output_dir, exist_ok=True)

    # -----------------------------
    # Caminhos
    # -----------------------------
    dem_path = os.path.join(data_dir, "SRTM_POA.tif")
    ndvi_path = os.path.join(data_dir, "NDVI_POA_February_2023.tif")

    slope_path = os.path.join(output_dir, "slope.tif")
    flood_risk_path = os.path.join(output_dir, "flood_risk.tif")
    risk_class_path = os.path.join(output_dir, "risk_class.tif")
    risk_class_smooth_path = os.path.join(output_dir, "risk_class_suavizado.tif")

    # -----------------------------
    # DEM
    # -----------------------------
    with rasterio.open(dem_path) as src:
        dem = src.read(1)
        profile = src.profile

    dem = mask_nodata(dem)

    # -----------------------------
    # Slope
    # -----------------------------
    print("Calculando slope...")
    wbt.slope(dem_path, slope_path, units="degrees")

    with rasterio.open(slope_path) as src:
        slope = src.read(1)

    slope = mask_nodata(slope)

    # -----------------------------
    # NDVI
    # -----------------------------
    ndvi = None

    if os.path.exists(ndvi_path):
        print("Carregando NDVI...")

        with rasterio.open(ndvi_path) as src:
            ndvi_raw = src.read(1)
            ndvi_profile = src.profile

        ndvi_raw = mask_nodata(ndvi_raw)

        aligned_ndvi = np.empty_like(dem)

        reproject(
            source=ndvi_raw,
            destination=aligned_ndvi,
            src_transform=ndvi_profile['transform'],
            src_crs=ndvi_profile['crs'],
            dst_transform=profile['transform'],
            dst_crs=profile['crs'],
            resampling=Resampling.bilinear
        )

        ndvi = aligned_ndvi

    else:
        print("NDVI não encontrado — usando apenas altimetria")

    # -----------------------------
    # RISCO
    # -----------------------------
    print("Calculando risco...")
    flood_risk = compute_flood_risk(dem, slope, ndvi)

    print("Suavizando risco...")
    flood_risk_smooth = smooth_risk(flood_risk, kernel_size=5)

    # -----------------------------
    # CLASSIFICAÇÃO
    # -----------------------------
    risk_class = classify_risk(flood_risk)
    risk_class_smooth = classify_risk(flood_risk_smooth)

    # -----------------------------
    # MAPA CONTÍNUO
    # -----------------------------
    plt.figure(figsize=(10, 6))
    cmap = plt.cm.RdYlGn_r
    cmap.set_bad(color='white')

    plt.imshow(flood_risk, cmap=cmap)
    plt.colorbar(label='nível de risco')
    plt.title('Mapa de Risco')

    plt.savefig(os.path.join(output_dir, "mapa_risco.png"), dpi=300)
    plt.show()

    # -----------------------------
    # MAPA SUAVIZADO CLASSIFICADO
    # -----------------------------
    plt.figure(figsize=(10, 6))

    cmap_class = plt.cm.get_cmap('RdYlGn_r', 3)

    plt.imshow(risk_class_smooth, cmap=cmap_class, vmin=1, vmax=3)
    plt.colorbar(ticks=[1, 2, 3], label='Classe de risco')
    plt.title('Mapa de Risco (Suavizado + Classificado)')

    plt.savefig(os.path.join(output_dir, "mapa_risco_suavizado.png"), dpi=300)
    plt.show()

    # -----------------------------
    # EXPORTAR RASTERS
    # -----------------------------
    profile.update(dtype=rasterio.float32, count=1, nodata=np.nan)

    with rasterio.open(flood_risk_path, "w", **profile) as dst:
        dst.write(flood_risk.astype(np.float32), 1)

    profile.update(dtype=rasterio.uint8, nodata=0)

    with rasterio.open(risk_class_path, "w", **profile) as dst:
        dst.write(risk_class, 1)

    with rasterio.open(risk_class_smooth_path, "w", **profile) as dst:
        dst.write(risk_class_smooth, 1)

    # -----------------------------
    # ÁREA POR CLASSE
    # -----------------------------
    print("Calculando área por classe...")

    valid_pixels = risk_class[risk_class > 0]

    unique, counts = np.unique(valid_pixels, return_counts=True)

    class_labels = {1: "Baixo", 2: "Médio", 3: "Alto"}

    labels = [class_labels[int(u)] for u in unique]

    pixel_size_x = profile['transform'][0]
    pixel_size_y = abs(profile['transform'][4])

    pixel_area = pixel_size_x * pixel_size_y

    areas_km2 = (counts * pixel_area) / 1e6

    plt.figure(figsize=(6, 6))
    plt.pie(areas_km2, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title("Área por Classe de Risco")

    plt.savefig(os.path.join(output_dir, "area_por_classe.png"), dpi=300)
    plt.show()

    print("Processamento concluído!")
    print(f"Saída em: {output_dir}")


if __name__ == "__main__":
    main()
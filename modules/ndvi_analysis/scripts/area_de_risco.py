import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt
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
    arr = arr.astype(float)
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
# MAIN
# -----------------------------
def main():

    # -----------------------------
    # Estrutura do projeto
    # -----------------------------
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
    ndvi_path = os.path.join(data_dir, "POA_ndvi_abril_2023.tif")

    slope_path = os.path.join(output_dir, "slope.tif")
    flood_risk_path = os.path.join(output_dir, "flood_risk.tif")
    risk_class_path = os.path.join(output_dir, "risk_class.tif")

    # -----------------------------
    # Verificação
    # -----------------------------
    if not os.path.exists(dem_path):
        raise FileNotFoundError(f"DEM não encontrado: {dem_path}")

    # -----------------------------
    # 1. Carregar DEM
    # -----------------------------
    with rasterio.open(dem_path) as src:
        dem = src.read(1)
        profile = src.profile

    dem = mask_nodata(dem)

    # -----------------------------
    # 2. Slope
    # -----------------------------
    print("Calculando slope...")
    wbt.slope(dem_path, slope_path, units="degrees")

    with rasterio.open(slope_path) as src:
        slope = src.read(1)

    slope = mask_nodata(slope)

    # -----------------------------
    # 3. NDVI
    # -----------------------------
    ndvi = None

    if os.path.exists(ndvi_path):
        print("Carregando NDVI...")

        with rasterio.open(ndvi_path) as src:
            ndvi_raw = src.read(1)
            ndvi_profile = src.profile

        ndvi_raw = mask_nodata(ndvi_raw)

        # Alinhamento espacial
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
    # 4. Modelo de risco
    # -----------------------------
    print("Calculando risco...")
    flood_risk = compute_flood_risk(dem, slope, ndvi)

    # -----------------------------
    # 5. Classificação
    # -----------------------------
    risk_class = classify_risk(flood_risk)

    # -----------------------------
    # 6. Visualização (com NaN transparente)
    # -----------------------------
    plt.figure(figsize=(10, 6))
    cmap = plt.cm.RdYlGn_r
    cmap.set_bad(color='white')  # NaN aparece branco (ou pode mudar)

    plt.imshow(flood_risk, cmap=cmap)
    plt.colorbar(label='nível de risco')
    plt.title('Mapa de Risco de Inundação')

    plt.savefig(os.path.join(output_dir, "mapa_risco.png"), dpi=300)
    plt.show()

    # -----------------------------
    # 7. Exportar raster de risco
    # -----------------------------
    profile.update(dtype=rasterio.float32, count=1, nodata=np.nan)

    with rasterio.open(flood_risk_path, "w", **profile) as dst:
        dst.write(flood_risk.astype(np.float32), 1)

    # -----------------------------
    # 8. Exportar classificação
    # -----------------------------
    profile.update(dtype=rasterio.uint8, count=1, nodata=0)

    with rasterio.open(risk_class_path, "w", **profile) as dst:
        dst.write(risk_class, 1)

    print("Processamento concluído!")
    print(f"Saída em: {output_dir}")


if __name__ == "__main__":
    main()
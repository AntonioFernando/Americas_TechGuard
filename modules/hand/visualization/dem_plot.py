# =========================================================
# DEM PLOT MODULE - VISUALIZAÇÃO
# =========================================================

from pathlib import Path
import rasterio
import numpy as np
import matplotlib.pyplot as plt

import rioxarray as rxr
import contextily as cx


# =========================================================
# PLOT SIMPLES (DEBUG / HEATMAP)
# =========================================================

def plot_dem(dem_path: Path, title="DEM - Elevação"):
    """
    Plot simples (rápido, sem basemap).
    """
    print("[DEM PLOT] Carregando DEM (modo simples)...")

    with rasterio.open(dem_path) as src:
        dem = src.read(1)

        if src.nodata is not None:
            dem = np.where(dem == src.nodata, np.nan, dem)

    plt.figure(figsize=(10, 8))
    img = plt.imshow(dem, cmap="terrain")
    plt.colorbar(img, label="Altitude (m)")

    plt.title(title)
    plt.axis("off")

    plt.tight_layout()
    plt.show()

    print("[DEM PLOT] Visualização simples concluída.")


# =========================================================
# PLOT AVANÇADO (COM BASEMAP)
# =========================================================

def plot_dem_with_basemap(dem_path: Path, title="DEM sobre satélite"):
    """
    Plot geoespacial com basemap (nível final do pipeline).
    """

    print("[DEM PLOT] Carregando DEM (modo geográfico)...")

    dem_path = str(dem_path) if isinstance(dem_path, Path) else dem_path

    # abre + reprojeta
    r = (
        rxr.open_rasterio(dem_path, masked=True)
        .squeeze()
        .rio.reproject(3857)
    )

    fig, ax = plt.subplots(figsize=(10, 10))

    print("[DEM PLOT] Renderizando raster...")

    img = r.plot(
        ax=ax,
        cmap="terrain",
        alpha=0.75,
        robust=True,
        add_colorbar=True
    )

    print("[DEM PLOT] Adicionando basemap...")

    cx.add_basemap(
        ax,
        source=cx.providers.Esri.WorldImagery,
        attribution_size=6
    )

    ax.set_axis_off()
    ax.set_title(title, fontsize=14, weight="bold")

    plt.tight_layout()
    plt.show()

    print("[DEM PLOT] Visualização com basemap concluída.")


# =========================================================
# EXPORT PNG (RELATÓRIO)
# =========================================================

def export_dem_png(dem_path: Path, out_png: Path, title="DEM"):
    """
    Exporta PNG simples para relatório.
    """

    print("[DEM PLOT] Exportando PNG...")

    with rasterio.open(dem_path) as src:
        dem = src.read(1)

        if src.nodata is not None:
            dem = np.where(dem == src.nodata, np.nan, dem)

    plt.figure(figsize=(10, 8))
    img = plt.imshow(dem, cmap="terrain")
    plt.colorbar(img, label="Altitude (m)")

    plt.title(title)
    plt.axis("off")

    plt.savefig(out_png, dpi=200, bbox_inches="tight")
    plt.close()

    print(f"[DEM PLOT] PNG salvo em: {out_png}")
# =========================================================
# RISK PLOT MODULE
# =========================================================
# Responsável por:
# - Visualizar classes HAND
# - Sobrepor ao mapa de satélite
# - Exportar PNG
# =========================================================

from pathlib import Path

import matplotlib.pyplot as plt
import rioxarray as rxr
import contextily as cx
from matplotlib.colors import ListedColormap


# =========================================================
# PLOT RISK
# =========================================================

def plot_risk(
    risk_path: Path,
    title="Mapa de Risco de Inundação"
):
    """
    Exibe raster classificado:
    0 = ALTO
    1 = MÉDIO
    2 = BAIXO
    3 = MUITO BAIXO
    """

    print("[RISK] Carregando raster...")

    r = (
        rxr.open_rasterio(
            risk_path,
            masked=True
        )
        .squeeze()
        .rio.reproject("EPSG:3857")
    )

    r_plot = r.where(r != 255)

    cmap = ListedColormap([
        "red",
        "orange",
        "yellow",
        "green"
    ])

    fig, ax = plt.subplots(
        figsize=(5, 14)
    )

    r_plot.plot(
        ax=ax,
        cmap=cmap,
        add_colorbar=True
    )

    cx.add_basemap(
        ax,
        source=cx.providers.Esri.WorldImagery,
        crs=r_plot.rio.crs
    )

    ax.set_title(
        title,
        fontsize=14,
        weight="bold"
    )

    ax.set_axis_off()

    plt.tight_layout()
    plt.show()

    print("[RISK] Visualização concluída.")

def export_risk_png(
    risk_path: Path,
    output_png: Path,
    title="Mapa de Risco"
):

    print("[RISK] Exportando PNG...")

    r = (
        rxr.open_rasterio(
            risk_path,
            masked=True
        )
        .squeeze()
        .rio.reproject("EPSG:3857")
    )

    r_plot = r.where(r != 255)

    cmap = ListedColormap([
        "red",
        "orange",
        "yellow",
        "green"
    ])

    fig, ax = plt.subplots(
        figsize=(10, 10)
    )

    r_plot.plot(
        ax=ax,
        cmap=cmap,
        add_colorbar=True
    )

    cx.add_basemap(
        ax,
        source=cx.providers.Esri.WorldImagery,
        crs=r_plot.rio.crs
    )

    ax.set_title(title)

    ax.set_axis_off()

    plt.tight_layout()

    plt.savefig(
        output_png,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"[RISK] PNG salvo em: {output_png}"
    )
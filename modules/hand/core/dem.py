# =========================================================
# DEM MODULE - HAND PIPELINE
# =========================================================

from pathlib import Path
import requests
import rasterio
from rasterio.mask import mask
import geopandas as gpd
from pystac_client import Client
import planetary_computer
import rioxarray as rxr
import matplotlib.pyplot as plt


# =========================================================
# ANADEM
# =========================================================

ANADEM_TILE = "22J"
ANADEM_URL = f"https://metadados.snirh.gov.br/files/anadem_v1_tiles/anadem_v1_{ANADEM_TILE}.tif"


def try_download_anadem(dst: Path) -> bool:
    print("\n[DEM] ===============================")
    print("[DEM] STEP 1 - ANADEM DOWNLOAD")
    print("[DEM] ===============================")

    try:
        print(f"[DEM] Tentando ANADEM tile {ANADEM_TILE}...")

        r = requests.get(
            ANADEM_URL,
            timeout=180,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        print(f"[DEM] HTTP status: {r.status_code}")

        if r.status_code != 200:
            print("[DEM] ANADEM indisponível -> fallback ativado")
            return False

        dst.write_bytes(r.content)

        print(f"[DEM] ANADEM salvo em: {dst}")
        return True

    except Exception as e:
        print(f"[DEM] ERRO ANADEM: {e}")
        print("[DEM] ativando fallback Copernicus...")
        return False


# =========================================================
# COPERNICUS DEM
# =========================================================

def download_copernicus_dem(dst: Path, bbox_4326):
    print("\n[DEM] ===============================")
    print("[DEM] STEP 2 - COPERNICUS FALLBACK")
    print("[DEM] ===============================")

    print(f"[DEM] BBOX 4326: {bbox_4326}")

    catalog = Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1"
    )

    search = catalog.search(
        collections=["cop-dem-glo-30"],
        bbox=bbox_4326
    )

    items = list(search.get_items())

    print(f"[DEM] Tiles encontrados: {len(items)}")

    if not items:
        raise RuntimeError("[DEM] Nenhum tile Copernicus encontrado")

    item = planetary_computer.sign(items[0])
    href = item.assets["data"].href

    print(f"[DEM] Downloading: {href}")

    dem = rxr.open_rasterio(href, masked=True).squeeze()
    dem.rio.to_raster(dst)

    print(f"[DEM] Copernicus salvo em: {dst}")


# =========================================================
# CLIP
# =========================================================

def clip_dem(dem_path: Path, union_gdf: gpd.GeoDataFrame, out_path: Path):

    print("\n[DEM] ===============================")
    print("[DEM] STEP 3 - CLIP DEM")
    print("[DEM] ===============================")

    with rasterio.open(dem_path) as src:

        print(f"[DEM] CRS DEM: {src.crs}")

        union_proj = union_gdf.to_crs(src.crs)
        geom = [union_proj.geometry.iloc[0].__geo_interface__]

        print("[DEM] Executando mask...")

        out_img, out_transform = mask(src, geom, crop=True)

        nodata = src.nodata if src.nodata is not None else -9999

        print("[DEM] Mask concluído")

        # 🚨 NÃO destruir dados
        out_img = out_img.astype("float32")

        meta = src.meta.copy()
        meta.update({
            "height": out_img.shape[1],
            "width": out_img.shape[2],
            "transform": out_transform,
            "dtype": "float32",
            "nodata": nodata
        })

        with rasterio.open(out_path, "w", **meta) as dst:
            dst.write(out_img)

    print(f"[DEM] Clip final salvo: {out_path}")


# =========================================================
# PNG
# =========================================================

def export_png(dem_path: Path, png_path: Path):
    print("\n[DEM] ===============================")
    print("[DEM] STEP 4 - EXPORT PNG")
    print("[DEM] ===============================")

    print(f"[DEM] Lendo: {dem_path}")

    with rasterio.open(dem_path) as src:
        data = src.read(1)

    print(f"[DEM] Shape: {data.shape}")
    print(f"[DEM] Min: {data.min()} | Max: {data.max()}")

    plt.figure(figsize=(8, 6))
    plt.imshow(data, cmap="terrain")
    plt.colorbar(label="Altitude")
    plt.title("DEM - Quicklook")
    plt.axis("off")

    plt.savefig(png_path, dpi=200, bbox_inches="tight")
    plt.close()

    print(f"[DEM] PNG salvo: {png_path}")


# =========================================================
# PIPELINE
# =========================================================

def build_dem(outdir: Path, union_gdf: gpd.GeoDataFrame) -> Path:

    print("\n[DEM] ====================================")
    print("[DEM] START BUILD DEM PIPELINE")
    print("[DEM] ====================================")

    outdir.mkdir(exist_ok=True)

    dem_raw = outdir / "dem_source.tif"
    dem_clip = outdir / "dem_contrib_clipped.tif"
    dem_png = outdir / "dem_quicklook.png"

    print(f"[DEM] Output dir: {outdir}")

    # -------------------------
    # DOWNLOAD
    # -------------------------
    if not dem_raw.exists():
        print("[DEM] DEM não existe -> iniciando download")

        ok = try_download_anadem(dem_raw)

        if not ok:
            print("[DEM] fallback ANADEM falhou -> Copernicus")
            union_4326 = union_gdf.to_crs(4326)
            bbox_4326 = union_4326.total_bounds.tolist()

            download_copernicus_dem(dem_raw, bbox_4326)

    else:
        print("[DEM] DEM já existe -> pulando download")

    # -------------------------
    # CLIP
    # -------------------------
    clip_dem(dem_raw, union_gdf, dem_clip)

    # -------------------------
    # PNG
    # -------------------------
    export_png(dem_clip, dem_png)

    print("\n[DEM] PIPELINE FINALIZADO COM SUCESSO")

    return dem_clip
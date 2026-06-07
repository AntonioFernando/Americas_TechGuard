from pathlib import Path
import geopandas as gpd

from core.ibge import (
    download_ibge,
    extract_ibge,
    load_municipalities,
    get_municipality
)

from core.snirh import query_ottobacias
from core.geometry import intersect, dissolve

from visualization.map import plot

from core.dem import build_dem
from core.hand import run_hand
from core.risk import classify_hand
from visualization.dem_plot import (
    plot_dem,
    plot_dem_with_basemap,
    export_dem_png
)

from visualization.risk_plot import (
    plot_risk,
    export_risk_png
)


def run_pipeline(outdir: Path, year=2023):

    outdir.mkdir(exist_ok=True)

    # ---------------- IBGE ----------------
    zip_path = download_ibge(year, outdir)
    extract_dir = extract_ibge(zip_path, outdir)

    mun = load_municipalities(extract_dir)
    blumenau = get_municipality(mun, "Blumenau").to_crs(4326)

    blum_3857 = blumenau.to_crs(3857)

    # ---------------- SNIRH ----------------
    xmin, ymin, xmax, ymax = blum_3857.total_bounds

    ottos = query_ottobacias((xmin, ymin, xmax, ymax))

    if ottos.crs != blum_3857.crs:
        ottos = ottos.to_crs(blum_3857.crs)

    ottos = intersect(ottos, blum_3857.geometry.iloc[0])

    if ottos.empty:
        raise ValueError("Sem ottobacias")

    # ---------------- UNION (FIX PRINCIPAL) ----------------
    union_geom = dissolve(ottos)

    union = gpd.GeoDataFrame(
        {"id": [1]},
        geometry=[union_geom],
        crs=ottos.crs
    )

    # ---------------- DEM ----------------
    dem_path = build_dem(outdir, union)

    #------------------HAND---------------

    hand_outdir = Path("outputs_hand")

    hand_data = run_hand(
        dem_path,
        hand_outdir
    )


    #---------------------RISK-----------------
    
    risk_path = classify_hand(
        hand_data["hand"],
        Path("outputs_hand") / "hand_risk.tif"
    )

    export_risk_png(
        risk_path,
        Path("outputs_hand") / "hand_risk.png"
    )

    # ---------------- VISUAL ----------------
    plot(ottos, "Ottobacias - Blumenau")

    # opcional (pipeline visual final)
    plot_dem(dem_path, "DEM - Blumenau")
    # plot_dem_with_basemap(dem_path)
    # export_dem_png(dem_path, outdir / "dem.png")

    plot_risk(risk_path, "Mapa de Susceptibilidade - Blumenau")

    return {
        "ottos": ottos,
        "union": union,
        "dem": dem_path,
        "hand": hand_data["hand"],
        "risk": risk_path
    }
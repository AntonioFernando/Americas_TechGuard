from pathlib import Path
import zipfile
import requests
import geopandas as gpd


def download_ibge(year: int, outdir: Path) -> Path:
    url = (
        "https://geoftp.ibge.gov.br/organizacao_do_territorio/"
        f"malhas_territoriais/malhas_municipais/municipio_{year}/UFs/SC/"
        f"SC_Municipios_{year}.zip"
    )

    zip_path = outdir / f"ibge_{year}.zip"

    if not zip_path.exists():
        print("[IBGE] baixando...")
        r = requests.get(url)
        r.raise_for_status()
        zip_path.write_bytes(r.content)

    return zip_path


def extract_ibge(zip_path: Path, outdir: Path) -> Path:
    extract_dir = outdir / "ibge_extract"

    if not extract_dir.exists():
        print("[IBGE] extraindo...")
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(extract_dir)

    return extract_dir


def load_municipalities(extract_dir: Path):
    shp = list(extract_dir.rglob("*.shp"))[0]
    return gpd.read_file(shp)


def get_municipality(gdf, name: str):
    mun_up = gdf["NM_MUN"].str.upper()

    return gdf[mun_up == name.upper()].copy()
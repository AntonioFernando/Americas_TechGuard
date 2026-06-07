from pathlib import Path
import time

import geopandas as gpd
import requests


def query_ottobacias(
    bbox,
    where="1=1",
    page_size=2000
):
    """
    Consulta ottobacias no SNIRH/ANA.

    Caso o serviço esteja indisponível:
    - tenta 3 vezes
    - utiliza cache local se existir
    """

    url = (
        "https://www.snirh.gov.br/arcgis/rest/services/"
        "SPR/BHO2017_50K_AREADRENAGEM/MapServer/0/query"
    )

    xmin, ymin, xmax, ymax = bbox

    backup_dir = Path("backup")
    backup_dir.mkdir(exist_ok=True)

    cache_file = backup_dir / "ottobacias_blumenau_raw.gpkg"

    max_retries = 3

    for attempt in range(max_retries):

        try:

            print(
                f"[SNIRH] Consulta online "
                f"(tentativa {attempt + 1}/{max_retries})..."
            )

            features = []
            offset = 0

            while True:

                params = {
                    "f": "geojson",
                    "where": where,
                    "geometry": (
                        f"{xmin},{ymin},{xmax},{ymax}"
                    ),
                    "geometryType": "esriGeometryEnvelope",
                    "inSR": 3857,
                    "outSR": 3857,
                    "returnGeometry": "true",
                    "resultRecordCount": page_size,
                    "resultOffset": offset,
                }

                r = requests.post(
                    url,
                    data=params,
                    timeout=5
                )

                r.raise_for_status()

                data = r.json()

                if "error" in data:
                    raise RuntimeError(
                        data["error"]
                    )

                page = data.get(
                    "features",
                    []
                )

                features.extend(page)

                if len(page) < page_size:
                    break

                offset += page_size

            if not features:
                raise RuntimeError(
                    "SNIRH retornou zero features."
                )

            gdf = gpd.GeoDataFrame.from_features(
                features,
                crs=3857
            )

            # -------------------------
            # Salvar cache automático
            # -------------------------

            try:

                gdf.to_file(
                    cache_file,
                    driver="GPKG"
                )

                print(
                    f"[SNIRH] Cache salvo: "
                    f"{cache_file}"
                )

            except Exception as cache_error:

                print(
                    "[SNIRH] Aviso: "
                    f"não foi possível salvar cache: "
                    f"{cache_error}"
                )

            return gdf

        except Exception as e:

            print(
                f"[SNIRH] Falha na tentativa "
                f"{attempt + 1}: {e}"
            )

            if attempt < max_retries - 1:

                print(
                    "[SNIRH] Aguardando "
                    "5 segundos..."
                )

                time.sleep(5)

    # ------------------------------------------------
    # Fallback para cache local
    # ------------------------------------------------

    if cache_file.exists():

        print(
            "\n[SNIRH] Serviço indisponível."
        )

        print(
            "[SNIRH] Utilizando cache local:"
        )

        print(
            f"        {cache_file}"
        )

        return gpd.read_file(
            cache_file
        )

    raise RuntimeError(
        "[SNIRH] Falha na consulta e "
        "nenhum cache local encontrado."
    )
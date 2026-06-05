import requests
import geopandas as gpd


def query_ottobacias(bbox, where="1=1", page_size=2000):
    url = "https://www.snirh.gov.br/arcgis/rest/services/SPR/BHO2017_50K_AREADRENAGEM/MapServer/0/query"

    xmin, ymin, xmax, ymax = bbox
    features = []
    offset = 0

    while True:
        params = {
            "f": "geojson",
            "where": where,
            "geometry": f"{xmin},{ymin},{xmax},{ymax}",
            "geometryType": "esriGeometryEnvelope",
            "inSR": 3857,
            "outSR": 3857,
            "returnGeometry": "true",
            "resultRecordCount": page_size,
            "resultOffset": offset,
        }

        r = requests.post(url, data=params)
        r.raise_for_status()
        data = r.json()

        page = data.get("features", [])
        features.extend(page)

        if len(page) < page_size:
            break

        offset += page_size

    return gpd.GeoDataFrame.from_features(features, crs=3857)
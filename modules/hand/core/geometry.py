from shapely.ops import unary_union
import geopandas as gpd


def intersect(gdf, geom):
    return gdf[gdf.intersects(geom)].copy()


def dissolve(gdf):
    return unary_union(gdf.geometry)


def to_gdf(geom, crs=3857):
    return gpd.GeoDataFrame({"id": [1]}, geometry=[geom], crs=crs)
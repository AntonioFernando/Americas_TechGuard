from pathlib import Path
import numpy as np
import xarray as xr
import rioxarray as rxr

from core.dem import build_dem
from core.hand import run_hand



def classify_hand(
    hand_path: Path,
    output_path: Path,
    thresholds=(5, 15, 40)
):
    print("\n[RISK] Classificando HAND...")

    t1, t2, t3 = thresholds

    r = (
        rxr.open_rasterio(hand_path, masked=True)
        .squeeze()
        .astype("float32")
    )

    valid = xr.where(np.isfinite(r), True, False)

    cls = xr.full_like(
        r,
        255,
        dtype="uint8"
    )

    cls = cls.where(
        ~(valid & (r <= t1)),
        0
    )

    cls = cls.where(
        ~(valid & (r > t1) & (r <= t2)),
        1
    )

    cls = cls.where(
        ~(valid & (r > t2) & (r <= t3)),
        2
    )

    cls = cls.where(
        ~(valid & (r > t3)),
        3
    )

    cls.rio.write_nodata(
        255,
        inplace=True
    )


    cls.rio.to_raster(output_path)

    print(
        f"[RISK] Raster salvo: {output_path}"
    )

    return output_path

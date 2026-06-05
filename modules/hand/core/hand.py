# =========================================================
# HAND MODULE
# =========================================================
# Responsável por:
# - Configuração do pipeline HAND
# - Validação dos parâmetros
# - Inicialização do WhiteboxTools
# - Definição dos arquivos de saída
# =========================================================
import os
from pathlib import Path
from whitebox.whitebox_tools import WhiteboxTools



# =========================================================
# VALIDADORES
# =========================================================

def positive_int(value):
    """
    Valida inteiro positivo.
    """
    value = int(value)

    if value <= 0:
        raise ValueError(
            f"Valor inválido ({value}). Deve ser > 0."
        )

    return value


def positive_float(value):
    """
    Valida float positivo.
    """
    value = float(value)

    if value <= 0:
        raise ValueError(
            f"Valor inválido ({value}). Deve ser > 0."
        )

    return value


# =========================================================
# THRESHOLD
# =========================================================

def calculate_threshold(
    threshold_cells=None,
    cellsize_m=None,
    area_km2=None
):
    """
    Calcula threshold final.
    """

    if threshold_cells is not None:
        threshold_cells = positive_int(threshold_cells)

    elif (
        cellsize_m is not None
        and area_km2 is not None
    ):
        cellsize_m = positive_float(cellsize_m)
        area_km2 = positive_float(area_km2)

        threshold_cells = int(
            (area_km2 * 1_000_000.0)
            / (cellsize_m ** 2)
        )

    else:
        raise ValueError(
            "Defina threshold_cells OU "
            "(cellsize_m e area_km2)"
        )

    print(f"[HAND] Threshold final: {threshold_cells}")

    return threshold_cells


# =========================================================
# WHITEBOX
# =========================================================

def setup_whitebox(outdir: Path):

    print("\n[HAND] Inicializando WhiteboxTools...")

    wbt = WhiteboxTools()

    wbt.set_verbose_mode(True)

    wbt.work_dir = str(
        outdir.resolve()
    )

    print(
        f"[HAND] Workdir: {wbt.work_dir}"
    )

    return wbt


# =========================================================
# PATHS
# =========================================================

def build_paths(
    outdir: Path,
    prefix="hand"
):
    """
    Define todos os caminhos usados pelo pipeline.
    """

    paths = {
        "dem_filled":
            outdir / f"{prefix}_dem_filled.tif",

        "flow_dir":
            outdir / f"{prefix}_d8_pointer.tif",

        "flow_acc":
            outdir / f"{prefix}_d8_accum.tif",

        "streams":
            outdir / f"{prefix}_streams.tif",

        "hand":
            outdir / f"{prefix}_hand.tif",
    }

    print("\n[HAND] Arquivos de saída:")

    for name, path in paths.items():
        print(f"   {name}: {path}")

    return paths


# =========================================================
# CONFIGURAÇÃO
# =========================================================

def create_hand_config(
    dem_path: Path,
    outdir: Path,
    prefix="hand",
    breach=True,
    threshold_cells=100,
    cellsize_m=None,
    area_km2=None,
    keep_intermediates=False,
    breach_dist=100
):
    """
    Cria e valida configuração do HAND.
    """

    print("\n[HAND] =================================")
    print("[HAND] CONFIGURAÇÃO")
    print("[HAND] =================================")

    if not dem_path.exists():
        raise FileNotFoundError(
            f"DEM não encontrado: {dem_path}"
        )

    print(f"[HAND] DEM: {dem_path}")

    outdir.mkdir(
        parents=True,
        exist_ok=True
    )

    print(f"[HAND] Saída: {outdir}")

    threshold = calculate_threshold(
        threshold_cells=threshold_cells,
        cellsize_m=cellsize_m,
        area_km2=area_km2
    )

    paths = build_paths(
        outdir,
        prefix
    )

    config = {
        "dem": dem_path,
        "outdir": outdir,
        "prefix": prefix,
        "breach": breach,
        "breach_dist": breach_dist, 
        "threshold_cells": threshold,
        "keep_intermediates": keep_intermediates,
        "paths": paths,
    }

    return config


# =========================================================
# PIPELINE HAND (placeholder)
# =========================================================

def run_hand(
    dem_path: Path,
    outdir: Path,
    prefix="hand",
    breach=True,
    breach_dist=100,
    threshold_cells=100,
    cellsize_m=None,
    area_km2=None,
    keep_intermediates=False
):

    config = create_hand_config(
    dem_path=dem_path,
    outdir=outdir,
    prefix=prefix,
    breach=breach,
    breach_dist=breach_dist,
    threshold_cells=threshold_cells,
    cellsize_m=cellsize_m,
    area_km2=area_km2,
    keep_intermediates=keep_intermediates
)

    wbt = setup_whitebox(
        config["outdir"]
    )

    hand_path = execute_hand(
        wbt,
        config
    )

    return {
        "config": config,
        "hand": hand_path
    }

def execute_hand(
    wbt,
    config
):
    """
    Executa o pipeline HAND usando WhiteboxTools.
    """

    print("\n[HAND] =================================")
    print("[HAND] EXECUTANDO PIPELINE HAND")
    print("[HAND] =================================")

    dem = str(config["dem"].resolve())

    breach = config["breach"]

    breach_dist = config["breach_dist"]

    threshold_cells = config["threshold_cells"]

    keep_intermediates = config["keep_intermediates"]

    paths = config["paths"]

    dem_filled = str(paths["dem_filled"].resolve())
    flow_dir = str(paths["flow_dir"].resolve())
    flow_acc = str(paths["flow_acc"].resolve())
    streams = str(paths["streams"].resolve())
    hand = str(paths["hand"].resolve())

    # ---------------------------------------------------
    # STEP 1
    # ---------------------------------------------------

    print("\n[1/6] Condicionando DEM...")

    if breach:

        print("[HAND] Método: BreachDepressionsLeastCost")

        wbt.breach_depressions_least_cost(
            dem=dem,
            output=dem_filled,
            dist=breach_dist
        )

    else:

        print("[HAND] Método: FillDepressions")

        wbt.fill_depressions(
            dem=dem,
            output=dem_filled
        )

    # ---------------------------------------------------
    # STEP 2
    # ---------------------------------------------------

    print("\n[2/6] Direção de fluxo D8...")

    wbt.d8_pointer(
        dem=dem_filled,
        output=flow_dir
    )

    # ---------------------------------------------------
    # STEP 3
    # ---------------------------------------------------

    print("\n[3/6] Acumulação D8...")

    wbt.d8_flow_accumulation(
        dem_filled,
        output=flow_acc,
        out_type="cells"
    )

    # ---------------------------------------------------
    # STEP 4
    # ---------------------------------------------------

    print(
        f"\n[4/6] Extraindo streams "
        f"(threshold={threshold_cells})..."
    )

    wbt.extract_streams(
        flow_accum=flow_acc,
        output=streams,
        threshold=threshold_cells
    )

    # ---------------------------------------------------
    # STEP 5
    # ---------------------------------------------------

    print("\n[5/6] Calculando HAND...")

    wbt.elevation_above_stream(
        dem=dem_filled,
        streams=streams,
        output=hand
    )

    # Verifica se o Whitebox realmente gerou o raster
    if not Path(hand).exists():
        raise RuntimeError(
            "[HAND] WhiteboxTools não gerou o arquivo HAND."
    )

    # ---------------------------------------------------
    # STEP 6
    # ---------------------------------------------------

    print(f"\n[6/6] HAND concluído.")

    print(f"[HAND] Arquivo gerado:")
    print(hand)

    # ---------------------------------------------------
    # LIMPEZA
    # ---------------------------------------------------

    if not keep_intermediates:

        print("\n[HAND] Removendo intermediários...")

        for fp in [
            dem_filled,
            flow_dir,
            flow_acc,
            streams
        ]:
            try:
                os.remove(fp)
            except Exception:
                pass

        print("[HAND] Intermediários removidos.")

    else:

        print(
            "\n[HAND] Intermediários mantidos."
        )

    return Path(hand)
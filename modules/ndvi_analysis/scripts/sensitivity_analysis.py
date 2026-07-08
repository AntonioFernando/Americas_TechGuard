import os

from flood_comparison_model import (
    compute_ndvi,
    runoff_from_ndvi_and_soil,
    simulate_rain_event,
)


# --------------------------------------------------------
# Executa um cenário
# --------------------------------------------------------
def run_scenario(name, rmax, alpha, beta,
                 rec_mean, fort_mean,
                 rec_soil, fort_soil):

    rec_runoff = runoff_from_ndvi_and_soil(
        rec_mean,
        rec_soil,
        rmax=rmax,
        alpha=alpha,
        beta=beta,
    )

    fort_runoff = runoff_from_ndvi_and_soil(
        fort_mean,
        fort_soil,
        rmax=rmax,
        alpha=alpha,
        beta=beta,
    )

    rec = simulate_rain_event(rec_runoff)
    fort = simulate_rain_event(fort_runoff)

    rec_peak = max(rec[3])
    fort_peak = max(fort[3])

    return {
        "Scenario": name,

        "Rec_Runoff": rec_runoff,
        "Fort_Runoff": fort_runoff,

        "Rec_Flood": rec[0],
        "Fort_Flood": fort[0],

        "Rec_Drain": rec[1],
        "Fort_Drain": fort[1],

        "Rec_Peak": rec_peak,
        "Fort_Peak": fort_peak,
    }


# --------------------------------------------------------
# Impressão formatada
# --------------------------------------------------------
def print_results(results):

    print("\n================ SENSITIVITY ANALYSIS ================\n")

    print(
        f"{'Scenario':<10}"
        f"{'Rec R':>10}"
        f"{'Fort R':>10}"
        f"{'Rec Flood':>12}"
        f"{'Fort Flood':>12}"
        f"{'Rec Drain':>12}"
        f"{'Fort Drain':>12}"
        f"{'Rec Peak':>12}"
        f"{'Fort Peak':>12}"
    )

    print("-" * 102)

    for r in results:

        print(
            f"{r['Scenario']:<10}"
            f"{r['Rec_Runoff']:>10.3f}"
            f"{r['Fort_Runoff']:>10.3f}"
            f"{r['Rec_Flood']:>12}"
            f"{r['Fort_Flood']:>12}"
            f"{r['Rec_Drain']:>12}"
            f"{r['Fort_Drain']:>12}"
            f"{r['Rec_Peak']:>12.1f}"
            f"{r['Fort_Peak']:>12.1f}"
        )


# --------------------------------------------------------
# Main
# --------------------------------------------------------
def main():

    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, "..", "..", ".."))
    data_dir = os.path.join(project_root, "data")

    rec_path = os.path.join(
        data_dir,
        "Recife_MSI_all_bands_20_agosto_2022.tif",
    )

    fort_path = os.path.join(
        data_dir,
        "Fort_Lauderdale_MSI_all_bands_apos_enchente_outubro.tif",
    )

    rec_mean, _ = compute_ndvi(rec_path)
    fort_mean, _ = compute_ndvi(fort_path)

    rec_soil = 0.2
    fort_soil = 0.8

    scenarios = [

        ("Low", 0.8, 0.4, 0.3),

        ("Base", 0.9, 0.6, 0.5),

        ("High", 1.0, 0.8, 0.7),

    ]

    results = []

    for name, rmax, alpha, beta in scenarios:

        results.append(

            run_scenario(
                name,
                rmax,
                alpha,
                beta,
                rec_mean,
                fort_mean,
                rec_soil,
                fort_soil,
            )

        )

    print_results(results)


if __name__ == "__main__":
    main()
import os
import numpy as np
import matplotlib.pyplot as plt
from ndvi_processing import load_multiband_raster, calculate_ndvi

# -----------------------------
# Runoff baseado em NDVI + solo
# -----------------------------
def runoff_from_ndvi_and_soil(ndvi_mean, soil_permeability):
    runoff = 0.9 - (ndvi_mean * 0.6)
    runoff *= (1 - 0.5 * soil_permeability)  # solo permeável reduz runoff
    runoff = np.clip(runoff, 0.05, 0.95)
    return runoff

# -----------------------------
# Simulação hidrológica
# -----------------------------
def simulate_rain_event(runoff_coef, rainfall_intensity=30, rainfall_duration=720,
                        flood_threshold=40, urban_drainage=5, max_minutes=10080):
    rainfall_per_min = rainfall_intensity / 60
    drainage_per_min = urban_drainage / 60

    water = 0
    flood_time = None
    drainage_time = None
    water_curve = []

    for minute in range(max_minutes):
        if minute < rainfall_duration:
            water += rainfall_per_min * runoff_coef
        else:
            water -= drainage_per_min

        if water < 0:
            water = 0

        water_curve.append(water)

        if flood_time is None and water >= flood_threshold:
            flood_time = minute

        if flood_time is not None and minute > rainfall_duration and water < 1:
            drainage_time = minute - rainfall_duration
            break

    return flood_time, drainage_time, runoff_coef, water_curve

# -----------------------------
# Calcular NDVI
# -----------------------------
def compute_ndvi(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
    raster = load_multiband_raster(filepath)
    band_red = raster[3]
    band_nir = raster[7]
    ndvi = calculate_ndvi(band_red, band_nir)
    ndvi_mean = np.nanmean(ndvi)
    ndvi_std = np.nanstd(ndvi)
    return ndvi_mean, ndvi_std

# -----------------------------
# Gráfico de curvas comparativas
# -----------------------------
def plot_flood_curve_comparison(rec_curve, fort_curve):
    max_len = max(len(rec_curve), len(fort_curve))
    rec_curve = rec_curve + [rec_curve[-1]] * (max_len - len(rec_curve))
    fort_curve = fort_curve + [fort_curve[-1]] * (max_len - len(fort_curve))

    minutes = list(range(max_len))

    plt.figure(figsize=(12,6))
    plt.plot(minutes, rec_curve, label="Recife", color="blue")
    plt.plot(minutes, fort_curve, label="Fort Lauderdale", color="green")
    plt.axhline(y=40, linestyle="--", color="red", label="Limiar de inundação")
    plt.xlabel("Tempo (min)")
    plt.ylabel("Água acumulada (mm)")
    plt.title("Comparação da evolução da inundação")
    plt.legend()
    plt.tight_layout()
    plt.show()

# -----------------------------
# Gráfico de barras comparativo
# -----------------------------
def plot_bar_comparison(rec_results, fort_results):
    cities = ["Recife", "Fort Lauderdale"]
    flood_times = [rec_results[0], fort_results[0]]
    drainage_times = [rec_results[1], fort_results[1]]

    x = np.arange(len(cities))
    width = 0.35

    plt.figure(figsize=(8,6))
    bars1 = plt.bar(x - width/2, flood_times, width, label="Tempo até inundação", color="skyblue")
    bars2 = plt.bar(x + width/2, drainage_times, width, label="Tempo até drenagem", color="orange")

    # Adiciona os valores em cima de cada barra
    for bar in bars1:
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20, f'{int(bar.get_height())}', 
                 ha='center', va='bottom', fontsize=10)
    for bar in bars2:
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20, f'{int(bar.get_height())}', 
                 ha='center', va='bottom', fontsize=10)

    plt.xticks(x, cities)
    plt.ylabel("Tempo (min)")
    plt.title("Comparação de inundação e drenagem entre cidades")
    plt.legend()
    plt.tight_layout()
    plt.show()

# -----------------------------
# Pipeline principal
# -----------------------------
def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, "..", "..", ".."))
    data_dir = os.path.join(project_root, "data")

    rec_path = os.path.join(data_dir, "Recife_MSI_all_bands_20_agosto_2022.tif")
    fort_path = os.path.join(data_dir, "Fort_Lauderdale_MSI_all_bands_apos_enchente_outubro.tif")

    # Calcula NDVI
    rec_mean, rec_std = compute_ndvi(rec_path)
    fort_mean, fort_std = compute_ndvi(fort_path)

    print("\n===== NDVI =====")
    print(f"Recife NDVI médio: {rec_mean:.3f}, desvio: {rec_std:.3f}")
    print(f"Fort Lauderdale NDVI médio: {fort_mean:.3f}, desvio: {fort_std:.3f}")

    # Coeficiente de permeabilidade do solo
    rec_soil = 0.2  # argiloso
    fort_soil = 0.8  # arenoso

    # Runoff
    rec_runoff = runoff_from_ndvi_and_soil(rec_mean, rec_soil)
    fort_runoff = runoff_from_ndvi_and_soil(fort_mean, fort_soil)

    # Simulação
    rec_results = simulate_rain_event(runoff_coef=rec_runoff)
    fort_results = simulate_rain_event(runoff_coef=fort_runoff)

    print("\n===== RESULTADOS HIDROLÓGICOS =====")
    print(f"Recife Runoff médio: {rec_runoff:.3f}")
    print(f"Recife inundação: {rec_results[0]} min")
    print(f"Recife drenagem: {rec_results[1]} min")

    print(f"\nFort Lauderdale Runoff médio: {fort_runoff:.3f}")
    print(f"Fort Lauderdale inundação: {fort_results[0]} min")
    print(f"Fort Lauderdale drenagem: {fort_results[1]} min")

    # Gráficos
    plot_flood_curve_comparison(rec_results[3], fort_results[3])
    plot_bar_comparison(rec_results, fort_results)

if __name__ == "__main__":
    main()
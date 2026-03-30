import os
import numpy as np
import matplotlib.pyplot as plt
from ndvi_processing import load_multiband_raster, calculate_ndvi

# -----------------------------
# Coeficientes de permeabilidade do solo
# -----------------------------
# Valores entre 0 (pouco permeável) e 1 (muito permeável)
soil_permeability = {
    "argiloso": 0.2,
    "silte": 0.3,
    "franco-argiloso": 0.4,
    "franco": 0.5,
    "arenoso-argiloso": 0.6,
    "arenoso-franco": 0.7,
    "arenoso": 0.8,
    "rocha": 0.05
}

# -----------------------------
# Runoff baseado em NDVI + solo
# -----------------------------
def runoff_from_ndvi_and_soil(ndvi_mean, soil_coef):
    runoff = 0.9 - (ndvi_mean * 0.6)
    runoff *= (1 - 0.5 * soil_coef)  # solo permeável reduz runoff
    return np.clip(runoff, 0.05, 0.95)

# -----------------------------
# Simulação hidrológica
# -----------------------------
def simulate_rain_event(runoff_coef, rainfall_intensity=27.4, rainfall_duration=1440,
                        flood_threshold=40, urban_drainage=5, max_minutes=14400):
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

        water = max(water, 0)
        water_curve.append(water)

        if flood_time is None and water >= flood_threshold:
            flood_time = minute

        if flood_time is not None and minute > rainfall_duration and water < 1:
            drainage_time = minute - rainfall_duration
            break

    # Garantir que as variáveis não sejam None
    if flood_time is None:
        flood_time = 0
    if drainage_time is None:
        drainage_time = 0

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
# Gráfico da evolução da inundação
# -----------------------------
def plot_flood_curve(water_curve, flood_threshold=40, city_name="Cidade"):
    minutes = list(range(len(water_curve)))

    plt.figure(figsize=(12,6))
    plt.plot(minutes, water_curve, label=city_name, color="blue")
    plt.axhline(y=flood_threshold, linestyle="--", color="red", label="Limiar de inundação")
    plt.xlabel("Tempo (min)")
    plt.ylabel("Água acumulada (mm)")
    plt.title(f"Evolução da inundação em {city_name}")
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

    file_path = os.path.join(data_dir, "Fort_Lauderdale_MSI_all_bands.tif")

    # Calcula NDVI
    ndvi_mean, ndvi_std = compute_ndvi(file_path)
    print("\n===== NDVI =====")
    print(f"Fort Lauderdale NDVI médio: {ndvi_mean:.3f}, desvio: {ndvi_std:.3f}")

    # Seleciona tipo de solo
    soil_type = "arenoso-franco"
    soil_coef = soil_permeability[soil_type]

    # Runoff
    runoff = runoff_from_ndvi_and_soil(ndvi_mean, soil_coef)

    # Simulação
    flood_time, drainage_time, runoff_coef, water_curve = simulate_rain_event(runoff_coef=runoff)

    print("\n===== RESULTADOS HIDROLÓGICOS =====")
    print(f"Fort Lauderdale Runoff médio: {runoff_coef:.3f}")
    print(f"Fort Lauderdale inundação: {flood_time} min (~{flood_time/60:.1f} h)")
    print(f"Fort Lauderdale drenagem: {drainage_time} min (~{drainage_time/60:.1f} h)")

    # Gráfico da inundação
    plot_flood_curve(water_curve, city_name="Fort Lauderdale")

if __name__ == "__main__":
    main()
# NDVI Analysis

## Comparative Assessment of NDVI as a Complementary Indicator of Urban Flood Susceptibility

This repository contains the scripts, workflows, and documentation developed for the comparative analysis of the Normalized Difference Vegetation Index (NDVI) in two urban study areas: **Recife, Pernambuco, Brazil, and Fort Lauderdale, Florida, United States**.

The project investigates how vegetation conditions, represented by NDVI, can contribute as a complementary indicator to the assessment of urban flood susceptibility. The analysis combines multispectral satellite imagery, geospatial processing, statistical metrics, and an empirical comparative runoff model.

The repository is part of the research developed within the **Americas TechGuard** project.

---

## 1. Research Objective

The main objective is to investigate the contribution of NDVI to the comparative assessment of urban flood susceptibility, considering its relationship with vegetation cover and the potential influence of vegetation on surface runoff.

The study uses satellite-derived NDVI information to:

- Characterize vegetation conditions in the selected urban areas.
- Calculate descriptive statistics and vegetation-class distributions.
- Estimate the spatial distribution of NDVI classes.
- Compare vegetation conditions between Recife and Fort Lauderdale.
- Investigate NDVI as a complementary variable in an empirical runoff model.
- Evaluate how variations in model parameters affect the comparative results through sensitivity analysis.

NDVI is treated as a **complementary indicator**, rather than an independent determinant of flooding. The empirical model is intended for comparative analysis and does not represent a calibrated hydrodynamic flood simulation.

## 2. Study Areas and Satellite Data

The research considers two urban study areas:

| Study area | Country | Main optical dataset |
|---|---|---|
| Recife, Pernambuco | Brazil | Sentinel-2, August 2022 |
| Fort Lauderdale, Florida | United States | Sentinel-2, October 2023 |

The optical imagery was obtained from the **Sentinel-2 Surface Reflectance Harmonized** collection in Google Earth Engine.

The Normalized Difference Vegetation Index is calculated using the red and near-infrared bands:

\[
NDVI = \frac{NIR - Red}{NIR + Red}
\]

For Sentinel-2 imagery, the calculation uses:

- **Band 4 (B4):** Red.
- **Band 8 (B8):** Near-Infrared.

The Sentinel-1 SAR dataset for Fort Lauderdale, acquired in April 2023, is also included in the project for complementary flood-event visualization. It is not used as an input to the empirical runoff model.

### Main data characteristics

| Dataset | Spatial resolution | Main application |
|---|---:|---|
| Sentinel-2 MSI | 10 m | NDVI calculation and vegetation analysis |
| Sentinel-1 SAR | 10 m | Complementary flood-event visualization |
| Copernicus DEM | 30 m | Topographic context |
| SoilGrids | 250 m | Soil-related information and permeability proxy |

The satellite acquisition dates and raster metadata should be consulted in the corresponding GeoTIFF files and the research dataset.

## 3. Repository Structure

The repository is organized into separate directories for satellite data processing, Google Earth Engine scripts, Python analysis, and supporting resources.

```text
ndvi_analysis/
│
│
├── gee/
│   ├── sentinel2_recife.js
│   ├── sentinel2_fort_lauderdale.js
│   └── sentinel1_fort_lauderdale.js
│
├── scripts/
│   ├── ndvi_processing.py
│   ├── ndvi_metricas.py
│   ├── ndvi_comparacao.py
│   ├── ndvi_sazonalidade.py
│   ├── compare_regions.py
│   ├── comparativo.py
│   ├── flood_comparison_model.py
│   ├── flood_model.py
│   ├── sensitivity_analysis.py
│   └── area_de_risco.py
│
└── README.md
```

*Note: The structure above illustrates the main project components. Additional files, outputs, and supporting resources may be present in the repository.*

## 4. Google Earth Engine Processing

The `gee/` directory contains the JavaScript scripts used to access and process satellite imagery through Google Earth Engine.

The scripts are organized according to the satellite data and study area:

| Script | Description |
|---|---|
| `sentinel2_recife.js` | Sentinel-2 imagery processing for Recife |
| `sentinel2_fort_lauderdale.js` | Sentinel-2 imagery processing for Fort Lauderdale |
| `sentinel1_fort_lauderdale.js` | Sentinel-1 SAR imagery processing for Fort Lauderdale |

These scripts define the image collections, spatial boundaries, temporal filters, and visualization and export procedures used to obtain the satellite datasets.

The exported GeoTIFF files are subsequently used by the Python scripts in the `scripts/` directory.

For further information, see [`gee/README.md`](gee/README.md).

## 5. Python Analysis

The `scripts/` directory contains the Python workflows developed for raster processing, NDVI calculation, statistical analysis, regional comparison, and empirical modeling.

The scripts cover different stages and purposes of the research, including the main comparative analysis and exploratory investigations.

The principal processing and analytical tasks include:

- Loading and processing multispectral GeoTIFF files.
- Calculating NDVI from Sentinel-2 red and near-infrared bands.
- Generating NDVI visualizations and thematic classifications.
- Calculating descriptive statistics.
- Estimating the area and percentage represented by NDVI classes.
- Comparing NDVI distributions between study areas and acquisition periods.
- Applying the empirical comparative runoff model.
- Evaluating model sensitivity to parameter variations.

Some scripts were developed for exploratory analyses and earlier experimental workflows. They are retained in the repository to preserve the development history and provide additional methodological context.

For individual script descriptions and execution instructions, see [`scripts/README.md`](scripts/README.md).

## 6. NDVI Classification and Statistical Metrics

Two classification schemes are used for different analytical purposes.

### 6.1. Visual NDVI classification

The visual classification implemented in `ndvi_processing.py` uses five intervals:

| Class | NDVI interval |
|---|---|
| 1 | -1.00 to -0.50 |
| 2 | -0.50 to 0.00 |
| 3 | 0.00 to 0.25 |
| 4 | 0.25 to 0.50 |
| 5 | 0.50 to 1.00 |

This classification is intended for map visualization and spatial interpretation of NDVI values.

### 6.2. Statistical and area-based classification

The metrics implemented in `ndvi_metricas.py` use four intervals:

| Category | NDVI interval |
|---|---|
| Water | NDVI < 0.00 |
| Bare soil | 0.00 ≤ NDVI < 0.20 |
| Moderate vegetation | 0.20 ≤ NDVI < 0.50 |
| Dense vegetation | NDVI ≥ 0.50 |

This classification is used to calculate class areas and their relative percentages.

The two classification schemes serve different purposes and should not be interpreted as identical classifications.

## 7. Empirical Comparative Runoff Model

The script `flood_comparison_model.py` implements the empirical model used in the comparative analysis.

The model estimates a runoff-related indicator based on NDVI and a soil permeability proxy:

\[
R = (R_{\max} - \alpha \cdot NDVI) \cdot (1 - \beta \cdot P_s)
\]

Where:

- \(R\) is the estimated runoff-related indicator.
- \(R_{\max}\) is the maximum reference runoff parameter.
- \(NDVI\) is the mean vegetation index.
- \(\alpha\) is the NDVI influence parameter.
- \(\beta\) is the soil-related influence parameter.
- \(P_s\) is the normalized soil permeability proxy.

The model is applied to both study areas using common baseline assumptions and alternative parameter configurations.

### 7.1. Sensitivity analysis

Three parameter configurations are considered:

| Scenario | \(R_{\max}\) | \(\alpha\) | \(\beta\) |
|---|---:|---:|---:|
| Low | 0.8 | 0.4 | 0.3 |
| Base | 0.9 | 0.6 | 0.5 |
| High | 1.0 | 0.8 | 0.7 |

The sensitivity analysis investigates how changes in the model parameters influence the comparative results.

### 7.2. Model limitations

The model is empirical and simplified. It is designed to explore comparative relationships between NDVI, soil-related assumptions, and runoff behavior.

It is not a physically based hydrological or hydrodynamic model, and its outputs should not be interpreted as calibrated predictions of actual flood depth, flood extent, or observed flood timing.

The model results depend on the assumptions and parameter values defined in the implementation.

## 8. Requirements

The Python workflows use geospatial and scientific computing libraries.

The main dependencies include:

- Python 3
- NumPy
- Rasterio
- Matplotlib
- OpenCV
- SciPy
- WhiteboxTools (for workflows that use terrain processing)

Additional dependencies may be required by individual scripts.

Google Earth Engine scripts are executed in the Google Earth Engine Code Editor. Local execution through the Earth Engine API requires the corresponding Python or JavaScript environment and authentication.

## 9. Running the Analysis

### 9.1. Satellite data acquisition

1. Open the corresponding JavaScript file in the Google Earth Engine Code Editor.
2. Review the study-area geometry and image collection filters.
3. Run the script.
4. Export the required imagery as GeoTIFF files.

### 9.2. Local Python processing

1. Clone or download the repository.
2. Create and activate a Python virtual environment.
3. Install the required dependencies.
4. Place the required raster datasets in the appropriate data directory.
5. Run the desired Python script from the `scripts/` directory.

Example using PowerShell:

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
pip install numpy rasterio matplotlib opencv-python scipy
```

Run an individual script:

```powershell
python ndvi_processing.py
```

Some scripts contain predefined input paths and study-area configurations. Review the paths and input filenames in the relevant script before execution.

## 10. Research Dataset and Reproducibility

The satellite datasets and supporting research materials are available through Zenodo:

**DOI:** https://doi.org/10.5281/zenodo.24237499

The dataset provides the raster inputs used in the research. The Python scripts and Google Earth Engine workflows document the processing and analysis procedures.

For reproducibility, users should consider the following:

- Use the same raster datasets and acquisition dates.
- Preserve the spatial reference systems and raster resolutions.
- Verify that input files correspond to the expected study areas.
- Use the parameter values specified in the relevant scripts.
- Distinguish between the visual NDVI classification and the statistical area-based classification.
- Interpret empirical model outputs in light of their assumptions and limitations.

## 11. Related Resources

- **Research repository:** [Americas TechGuard](https://github.com/AntonioFernando/Americas_TechGuard)
- **Research dataset:** [Zenodo – DOI 10.5281/zenodo.24237499](https://doi.org/10.5281/zenodo.24237499)
- **Google Earth Engine:** [Official documentation](https://developers.google.com/earth-engine/guides)
- **Sentinel-2:** [Copernicus Sentinel-2 mission](https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2)
- **Sentinel-1:** [Copernicus Sentinel-1 mission](https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-1)

---

## 12. Citation

If you use the datasets, scripts, or methodological workflow from this repository, please cite the associated research dataset:

Souza, A. F. L. M. (2026). *Americas TechGuard – NDVI Analysis Research Dataset*. Zenodo. https://doi.org/10.5281/zenodo.24237499

Please verify the final bibliographic metadata against the Zenodo record before using this citation in a formal publication.
# Python Scripts – NDVI Analysis

This directory contains the Python scripts developed for raster processing, NDVI calculation, statistical analysis, spatial comparison, and empirical runoff modeling within the NDVI Analysis research project.

The scripts support the comparative investigation of NDVI as a complementary indicator of urban flood susceptibility in Recife, Brazil, and Fort Lauderdale, United States.

The directory includes both scripts directly associated with the research article and exploratory scripts developed during the project's methodological development. These scripts are retained to document the analytical workflow and preserve the progression of the research.

---

## 1. Directory Contents

| Script | Main purpose | Analytical category |
|---|---|---|
| `ndvi_processing.py` | Raster loading, NDVI calculation, visual classification, and mapping | NDVI processing |
| `ndvi_metricas.py` | Descriptive statistics and area calculation by NDVI class | Statistical analysis |
| `ndvi_comparacao.py` | Temporal comparison of NDVI datasets | Comparative analysis |
| `ndvi_sazonalidade.py` | Exploratory comparison of NDVI across different periods | Exploratory analysis |
| `compare_regions.py` | Spatial comparison between Recife and Fort Lauderdale | Main research analysis |
| `comparativo.py` | Visualization of previously calculated regional statistics | Statistical visualization |
| `flood_comparison_model.py` | Empirical comparative runoff and flood-accumulation model | Main research model |
| `flood_model.py` | Earlier experimental single-region runoff model | Exploratory modeling |
| `sensitivity_analysis.py` | Evaluation of changes in empirical model parameters | Sensitivity analysis |
| `area_de_risco.py` | Exploratory terrain and NDVI-based spatial classification | Exploratory geospatial modeling |

## 2. Script Documentation

### 2.1. `ndvi_processing.py`

**Purpose:** Process multispectral satellite imagery and calculate the Normalized Difference Vegetation Index (NDVI).

The script loads a multispectral raster, extracts the red and near-infrared bands, calculates NDVI, and generates visual outputs for spatial interpretation.

Main operations include:

- Loading multispectral GeoTIFF imagery.
- Extracting the red and near-infrared bands.
- Calculating NDVI.
- Applying a visual classification with five NDVI intervals.
- Applying median filtering to the classified raster.
- Generating NDVI maps and histograms.

The visual classification uses the following intervals:

| Class | NDVI interval |
|---|---|
| 1 | -1.00 to -0.50 |
| 2 | -0.50 to 0.00 |
| 3 | 0.00 to 0.25 |
| 4 | 0.25 to 0.50 |
| 5 | 0.50 to 1.00 |

This classification is intended for map visualization and spatial interpretation.

**Main input:** Multispectral Sentinel-2 GeoTIFF imagery.

**Outputs:** NDVI visualizations, classified maps, and histograms.

### 2.2. `ndvi_metricas.py`

**Purpose:** Calculate descriptive statistics and estimate the area represented by different NDVI classes.

The script provides quantitative metrics for characterizing vegetation conditions in the study area.

The main statistical indicators include:

- Mean.
- Median.
- Standard deviation.
- Variance.
- 10th and 90th percentiles.
- 25th and 75th percentiles.

The script also calculates the spatial area and percentage associated with four NDVI categories:

| Category | NDVI interval |
|---|---|
| Water | NDVI < 0.00 |
| Bare soil | 0.00 ≤ NDVI < 0.20 |
| Moderate vegetation | 0.20 ≤ NDVI < 0.50 |
| Dense vegetation | NDVI ≥ 0.50 |

These intervals are used for statistical and area-based analysis. They are intentionally different from the five-class visual classification implemented in `ndvi_processing.py`.

**Main input:** NDVI raster.

**Outputs:** Descriptive statistics and area distribution by NDVI category.

### 2.3. `ndvi_comparacao.py`

**Purpose:** Compare NDVI datasets from different acquisition periods.

This script performs a temporal comparison using NDVI rasters from different dates. It calculates descriptive statistics, evaluates the distribution of NDVI classes, and generates comparative visualizations.

Main operations include:

- Loading NDVI rasters from different periods.
- Calculating descriptive statistics.
- Comparing the area represented by NDVI classes.
- Generating NDVI distribution charts.
- Calculating and visualizing the difference between NDVI datasets.

**Main inputs:** NDVI GeoTIFF files from different acquisition periods.

**Outputs:** Comparative statistics, distribution charts, and an NDVI difference map.

**Note:** Raster comparison requires compatible spatial grids. Input rasters should have matching dimensions, spatial reference systems, and pixel alignment before pixel-by-pixel difference calculations.

### 2.4. `ndvi_sazonalidade.py`

**Purpose:** Perform exploratory comparisons of NDVI across different acquisition periods.

This script was developed to investigate changes in vegetation conditions between different dates. It supports exploratory temporal analysis and visualization.

The script reflects an experimental stage of the project, during which different datasets and acquisition periods were investigated.

It is retained as part of the research development history and should be interpreted according to the input files and configurations defined in its implementation.

**Main inputs:** NDVI rasters from different acquisition periods.

**Outputs:** Comparative visualizations and temporal NDVI analysis.

**Note:** This script is exploratory and is not the principal temporal analysis workflow used in the comparative research article.

### 2.5. `compare_regions.py`

**Purpose:** Perform a spatial comparison of NDVI characteristics between Recife and Fort Lauderdale.

This script supports the principal regional comparison presented in the research article.

It calculates and compares NDVI statistics and the percentage distribution of vegetation classes in the two study areas.

Main operations include:

- Loading the regional NDVI datasets.
- Calculating summary statistics.
- Comparing NDVI class percentages.
- Generating regional comparison charts.

The main comparison uses the Recife August 2022 dataset and the Fort Lauderdale October 2023 dataset.

**Main inputs:**

- Recife NDVI raster, August 2022.
- Fort Lauderdale NDVI raster, October 2023.

**Outputs:** Comparative statistical results and `comparacao_classes_ndvi.png`.

### 2.6. `comparativo.py`

**Purpose:** Generate a statistical visualization of regional NDVI results.

Unlike the raster-processing scripts, this script uses previously calculated summary statistics to produce a comparative boxplot.

It is intended to visualize and communicate differences in NDVI distributions between the study areas.

**Main inputs:** Previously calculated statistical values.

**Outputs:** Comparative boxplot.

**Note:** The statistics used by this script should be consistent with the corresponding source analysis. The script does not independently calculate NDVI from satellite imagery.

### 2.7. `flood_comparison_model.py`

**Purpose:** Implement the empirical comparative runoff model used in the research article.

This script evaluates the relationship between NDVI, a normalized soil permeability proxy, and an estimated runoff coefficient for Recife and Fort Lauderdale.

The model is defined as:

$$
R = (R_{\max} - \alpha \cdot NDVI) \cdot (1 - \beta \cdot P_s)
$$

Where:

- \(R\) is the estimated runoff coefficient.
- \(R_{\max}\) is the maximum reference runoff parameter.
- \(NDVI\) is the mean vegetation index.
- \(\alpha\) is the NDVI influence parameter.
- \(\beta\) is the soil-related influence parameter.
- \(P_s\) is the normalized soil permeability proxy.

The baseline parameter configuration is:

| Parameter | Value |
|---|---:|
| \(R_{\max}\) | 0.9 |
| \(\alpha\) | 0.6 |
| \(\beta\) | 0.5 |

The soil permeability proxies adopted in the comparative model are:

| Study area | Soil proxy |
|---|---:|
| Recife | 0.2 |
| Fort Lauderdale | 0.8 |

The script also implements a simplified rainfall and surface-water accumulation simulation.

The simulation uses:

- Constant rainfall intensity of 30 mm/h.
- Rainfall duration of 720 minutes (12 hours).
- A one-minute simulation time step.
- A drainage rate of 5 mm/h after rainfall ends.
- A surface-water accumulation threshold of 40 mm.

The water-balance calculation prevents simulated surface-water accumulation from becoming negative.

The script also evaluates alternative empirical parameter configurations and generates comparative plots.

**Main inputs:**

- Recife NDVI raster, August 2022.
- Fort Lauderdale NDVI raster, October 2023.

**Outputs:** Runoff coefficients, simulated accumulation curves, comparative results, and model visualizations.

**Research relevance:** This is the principal empirical model implemented for the comparative analysis in the research article.

**Important limitation:** The model is empirical and simplified. Its outputs represent simulated responses under prescribed rainfall and drainage assumptions. They are not calibrated hydrodynamic predictions or direct observations of actual flood onset, water depth, or drainage time.

### 2.8. `flood_model.py`

**Purpose:** Implement an earlier experimental runoff model for a single study area.

This script represents an earlier stage of the project's empirical modeling development.

It applies a simplified runoff formulation using NDVI and a soil-related coefficient. It also includes a rainfall-driven surface-water accumulation simulation and visualization.

The script contains a soil classification scheme with predefined coefficients for different soil types, including clay, silt, loam, sandy-loam, sand, and rock.

Its configuration differs from the later comparative model, including different rainfall assumptions and parameter constraints.

**Main inputs:** NDVI data and predefined soil-related parameters for the experimental study area.

**Outputs:** Runoff estimates and surface-water accumulation visualizations.

**Note:** This script is retained as an experimental and historical implementation. It is distinct from `flood_comparison_model.py`, which implements the comparative model used in the research article.

### 2.9. `sensitivity_analysis.py`

**Purpose:** Investigate how variations in empirical model parameters influence the estimated runoff coefficient.

The sensitivity analysis evaluates three parameter configurations:

| Scenario | \(R_{\max}\) | \(\alpha\) | \(\beta\) |
|---|---:|---:|---:|
| Low | 0.8 | 0.4 | 0.3 |
| Base | 0.9 | 0.6 | 0.5 |
| High | 1.0 | 0.8 | 0.7 |

The analysis examines how the selected parameter values affect the modeled runoff response in the two study areas.

The corresponding runoff coefficients reported in the research are:

| Study area | Low | Base | High |
|---|---:|---:|---:|
| Recife | 0.640 | 0.649 | 0.655 |
| Fort Lauderdale | 0.452 | 0.356 | 0.260 |

The results indicate that the relative runoff contrast between the two study areas is preserved across the tested configurations.

**Main inputs:** Regional NDVI statistics and empirical model parameters.

**Outputs:** Sensitivity results and comparative visualizations.

**Note:** Sensitivity analysis evaluates the behavior of the selected empirical formulation. It does not establish that the parameter values are physically calibrated or optimal.

### 2.10. `area_de_risco.py`

**Purpose:** Perform an exploratory geospatial analysis combining terrain characteristics and NDVI.

This script represents a separate exploratory workflow developed to investigate the relationship between elevation, slope, and vegetation conditions in relation to potential flood-related spatial patterns.

The implementation uses:

- Digital Elevation Model (DEM) data.
- NDVI raster data.
- Terrain slope derived using WhiteboxTools.
- Raster normalization and spatial alignment.
- Weighted combination of environmental variables.
- Classification and spatial filtering.

When NDVI is available, the implemented weighting scheme is:

| Variable | Weight |
|---|---:|
| NDVI | 0.4 |
| Elevation | 0.4 |
| Slope | 0.2 |

When NDVI is unavailable, the script uses an alternative combination of elevation and slope.

The resulting index is divided into three classes:

| Class | Index interval |
|---|---|
| Low | Below 0.30 |
| Moderate | 0.30–0.60 |
| High | 0.60 or above |

The workflow also includes raster reprojection and filtering operations.

**Main inputs:** DEM and NDVI raster datasets for the exploratory Porto Alegre analysis.

**Outputs:** Slope raster, combined index raster, classified raster, filtered classification, maps, and area charts.

**Important distinction:** This script is an exploratory terrain-based classification workflow. It is not the empirical comparative runoff model used in the Recife–Fort Lauderdale research article, and its classification should not be interpreted as a validated flood-risk map.

---

## 3. Relationship Between the Main Scripts

The principal processing and comparative analysis workflows can be understood as the following sequence:

```text
Sentinel-2 Multispectral Imagery
              |
              v
      ndvi_processing.py
              |
              v
          NDVI Raster
              |
              +----------------------+
              |                      |
              v                      v
      ndvi_metricas.py        compare_regions.py
              |                      |
              v                      v
     NDVI Statistics       Regional Comparison
              |                      |
              +----------+-----------+
                         |
                         v
              flood_comparison_model.py
                         |
                         v
              Comparative Runoff Model
                         |
                         v
               sensitivity_analysis.py
                         |
                         v
              Sensitivity Evaluation
```

The diagram represents the conceptual relationship between the main analytical components. Individual scripts may load their input rasters directly rather than depending on the execution of another script.

## 4. Software Requirements

The scripts use Python and scientific/geospatial libraries.

The main dependencies include:

| Library | Application |
|---|---|
| NumPy | Numerical operations and array processing |
| Rasterio | Raster data access and geospatial metadata |
| Matplotlib | Charts and visualizations |
| OpenCV | Image filtering and raster processing |
| SciPy | Scientific and spatial processing |
| WhiteboxTools | Terrain analysis in exploratory workflows |

Some scripts may require additional packages depending on their specific implementation.

### 4.1. Environment setup

Create and activate a Python virtual environment:

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

Install the main dependencies:

```powershell
pip install numpy rasterio matplotlib opencv-python scipy
```

For scripts that use WhiteboxTools, install the corresponding package:

```powershell
pip install whitebox
```

Additional dependencies should be installed when required by the individual scripts.

## 5. Execution

Run the scripts from the `scripts/` directory.

Example:

```powershell
python ndvi_processing.py
```

Other scripts can be executed individually:

```powershell
python ndvi_metricas.py
python compare_regions.py
python flood_comparison_model.py
python sensitivity_analysis.py
```

Some scripts contain predefined input paths and filenames. Before execution, verify that the raster files are available and that the paths correspond to the local directory structure.

The scripts are not necessarily designed to run as a single automated pipeline. Each one performs a specific analytical task and may require its own input configuration.

## 6. Input Data

The main raster datasets used in the comparative research include:

| Dataset | Study area | Application |
|---|---|---|
| Sentinel-2 multispectral imagery | Recife | NDVI calculation |
| Sentinel-2 multispectral imagery | Fort Lauderdale | NDVI calculation |
| Sentinel-1 SAR imagery | Fort Lauderdale | Complementary flood-event visualization |
| Digital Elevation Model | Depending on workflow | Terrain analysis |
| Soil-related information | Recife and Fort Lauderdale | Soil permeability proxy |

The research raster datasets and supporting materials are available through the associated Zenodo record:

https://doi.org/10.5281/zenodo.24412207

The acquisition dates, spatial reference systems, raster dimensions, and other technical properties should be verified from the corresponding GeoTIFF metadata.

## 7. Research Reproducibility and Interpretation

The scripts were developed for different analytical purposes throughout the research.

For reproducibility, it is important to distinguish between:

1. **Main research workflows:** Scripts used to calculate NDVI metrics, compare the two study areas, and implement the empirical comparative runoff model.
2. **Supporting visualizations:** Scripts that generate charts from previously calculated statistics.
3. **Exploratory workflows:** Scripts developed to investigate temporal variations, earlier runoff formulations, and terrain-related spatial patterns.

The presence of exploratory scripts does not imply that all their outputs were incorporated into the research article.

In particular:

- The visual NDVI classification and the statistical area-based classification use different intervals because they serve different analytical purposes.
- The Sentinel-1 SAR workflow provides complementary flood-event visualization and is not an input to the empirical runoff model.
- The single-region `flood_model.py` is an earlier experimental implementation, distinct from the comparative `flood_comparison_model.py`.
- The `area_de_risco.py` workflow is a separate exploratory analysis and does not represent the article's comparative runoff methodology.
- Empirical runoff and accumulation outputs should be interpreted according to their prescribed model assumptions, not as observations of actual flood conditions.

These distinctions are important when reproducing the results or extending the research.

## 8. Related Documentation and Resources

For additional information, consult:

- [`../README.md`](../README.md) – Main repository documentation.
- [`../gee/README.md`](../gee/README.md) – Google Earth Engine scripts and satellite data acquisition.
- [Americas TechGuard GitHub repository](https://github.com/AntonioFernando/Americas_TechGuard)
- [Research dataset on Zenodo](https://doi.org/10.5281/zenodo.24412207)

---

**Project:** Americas TechGuard – NDVI Analysis

**Research focus:** Comparative assessment of NDVI as a complementary indicator of urban flood susceptibility.

**Study areas:** Recife, Brazil, and Fort Lauderdale, United States.
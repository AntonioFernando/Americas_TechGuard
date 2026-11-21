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


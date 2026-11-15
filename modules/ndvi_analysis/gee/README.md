# Google Earth Engine Data Acquisition

## 1. Overview

This directory contains the Google Earth Engine (GEE) JavaScript scripts used to retrieve and prepare satellite imagery for the NDVI analysis module of the Americas TechGuard project.

The scripts cover two study areas:

- Recife, Pernambuco, Brazil.
- Fort Lauderdale, Florida, United States.

Two satellite missions are represented:

- **Sentinel-2 Multispectral Instrument (MSI):** optical imagery used for vegetation analysis and NDVI processing.
- **Sentinel-1 Synthetic Aperture Radar (SAR):** radar imagery used for visual inspection and illustration of the Fort Lauderdale flooding event in April 2023.

The exported GeoTIFF files are subsequently processed by the Python scripts located in the `scripts/` directory.

The satellite datasets and associated research materials are publicly available through the project's Zenodo repository:

**Dataset DOI:** [https://doi.org/10.5281/zenodo.24237499](https://doi.org/10.5281/zenodo.24237499)

## 2. Directory Contents

| Script | Satellite dataset | Study area | Main purpose |
|---|---|---|---|
| `sentinel2_recife.js` | Sentinel-2 MSI | Recife, Brazil | Optical imagery acquisition for NDVI analysis |
| `sentinel2_fort_lauderdale.js` | Sentinel-2 MSI | Fort Lauderdale, USA | Optical imagery acquisition for NDVI analysis |
| `sentinel1_fort_lauderdale.js` | Sentinel-1 SAR | Fort Lauderdale, USA | Radar imagery acquisition for flood-event visualization |

## 3. Sentinel-2: Recife, Brazil

**Script:** `sentinel2_recife.js`

### Dataset

- Collection: `COPERNICUS/S2_SR_HARMONIZED`
- Satellite: Sentinel-2
- Instrument: Multispectral Instrument (MSI)
- Study period configured in the script: August 1–30, 2022
- Spatial resolution of the principal bands: 10 m

### Selected bands

| Band | Description | Role |
|---|---|---|
| B2 | Blue | True-color visualization |
| B3 | Green | True-color visualization |
| B4 | Red | NDVI calculation and visualization |
| B8 | Near Infrared (NIR) | NDVI calculation and visualization |

The script also retains the available Sentinel-2 bands when preparing the multispectral GeoTIFF export.

### Image filtering and cloud masking

The image collection is filtered using:

- Acquisition period.
- Study-area geometry.
- `CLOUDY_PIXEL_PERCENTAGE` below 5%.

An additional pixel-level cloud and shadow masking procedure is applied using the Scene Classification Layer (SCL).

The following SCL classes are excluded:

| SCL class | Description |
|---|---|
| 3 | Cloud shadow |
| 8 | Cloud medium probability |
| 9 | Cloud high probability |
| 10 | Thin cirrus |
| 11 | Snow or ice |

The masking function is applied to the collection using `.map(maskS2clouds)`.

### Image selection

The script selects the first image returned by the filtered collection using `.first()`.

This selection procedure is part of the original image retrieval workflow.

### Export

The script provides an export configuration for the complete multispectral image:

- Export description: `Recife_MSI_all_bands`
- Export format: GeoTIFF
- Pixel type: UInt16
- Spatial scale: 10 m
- Export region: defined study-area geometry

The export command is commented out in the original script and must be enabled when a new export is required.

## 4. Sentinel-2: Fort Lauderdale, United States

**Script:** `sentinel2_fort_lauderdale.js`

### Dataset

- Collection: `COPERNICUS/S2_SR_HARMONIZED`
- Satellite: Sentinel-2
- Instrument: Multispectral Instrument (MSI)
- Study period configured in the script: March 3–16, 2023
- Spatial resolution of the principal bands: 10 m

### Selected bands

| Band | Description | Role |
|---|---|---|
| B2 | Blue | True-color visualization |
| B3 | Green | True-color visualization |
| B4 | Red | NDVI calculation and visualization |
| B8 | Near Infrared (NIR) | NDVI calculation and visualization |

### Image filtering

The image collection is filtered by:

- Acquisition period.
- Study-area geometry.
- `CLOUDY_PIXEL_PERCENTAGE` below 5%.

Unlike the Recife script, this script does not apply an additional SCL-based pixel-level cloud mask.

### Image selection

The script selects the first image returned by the filtered collection using `.first()`.

This procedure follows the original image selection workflow used for the Fort Lauderdale study area.

### Export

The script provides an export configuration for the complete multispectral image:

- Export description: `Fort_Lauderdale_MSI_all_bands`
- Export format: GeoTIFF
- Pixel type: UInt16
- Spatial scale: 10 m
- Export region: defined study-area geometry

The script also contains an alternative export configuration for selected optical bands.

The export commands are commented out in the original script and must be enabled when a new export is required.

## 5. Sentinel-1: Fort Lauderdale, United States

**Script:** `sentinel1_fort_lauderdale.js`

### Dataset

- Collection: `COPERNICUS/S1_GRD`
- Satellite: Sentinel-1
- Instrument: C-band Synthetic Aperture Radar (SAR)
- Acquisition period configured in the script: April 11–14, 2023
- Instrument mode: Interferometric Wide (IW)

### Polarizations

| Band | Description |
|---|---|
| VV | Vertical transmit, vertical receive |
| VH | Vertical transmit, horizontal receive |

The collection is filtered by the presence of the VV polarization and by the IW acquisition mode.

Both VV and VH are selected for visualization and export.

### Visualization

The script displays the VV and VH polarization bands using a visualization range from -25 to 0 dB.

### Export

The script provides an export configuration with the following settings:

- Export description: `Fort_Lauderdale_SAR`
- Export format: GeoTIFF
- Selected bands: VV and VH
- Spatial scale: 10 m
- Export region: defined study-area geometry

The export command is commented out in the original script and must be enabled when a new export is required.

### Role in the research

Sentinel-1 imagery was used for visual inspection and illustration of the Fort Lauderdale flooding event in April 2023.

**The Sentinel-1 data are not used as input variables in the comparative empirical runoff model.** The model calculations are based on the optical NDVI data and the soil-related parameters described in the main module documentation.

## 6. Data Export and Relationship with Python Processing

The GEE scripts provide the satellite imagery used by the Python processing workflow.

The general data flow is:

1. Define the study-area geometry.
2. Retrieve the corresponding satellite image collection.
3. Apply the temporal, spatial, and other dataset-specific filters.
4. Select the image used in the analysis.
5. Prepare the required bands and data type.
6. Export the image as a GeoTIFF.
7. Process the exported raster using the Python scripts in `scripts/`.

The principal optical bands used for NDVI calculation are:

- **B4:** Red.
- **B8:** Near Infrared (NIR).

The NDVI calculation is performed in the Python processing workflow, rather than being calculated directly in these GEE acquisition scripts.

The exported GeoTIFF files are maintained in the project's data directory. Their metadata provide the definitive information about the actual raster files used in the analysis, including acquisition-related information, spatial reference, dimensions, resolution, and band configuration.

The configured date ranges in the JavaScript scripts describe the image collection search periods. They should not be interpreted as the exact acquisition dates of the final exported rasters.

## 7. Execution Requirements and Reproducibility

### 7.1. Google Earth Engine execution

The JavaScript scripts in this directory were developed for the Google Earth Engine environment.

The original execution environment is the [Google Earth Engine Code Editor](https://code.earthengine.google.com/), which provides access to the Earth Engine data catalog, image collections, geospatial processing functions, map visualization, and export tasks.

Users who want to reproduce the satellite imagery acquisition stage can:

1. Access the Google Earth Engine Code Editor.
2. Authenticate with an eligible Google account and configure the required Earth Engine access.
3. Open or copy the corresponding JavaScript script.
4. Execute the script in the Code Editor.
5. Enable the relevant export command when a new GeoTIFF file is required.

The `.js` files should not be interpreted as standalone JavaScript programs that can be executed directly with Node.js without additional configuration. They use Earth Engine-specific objects and functions, including `ee.ImageCollection`, `ee.Geometry`, `Map.addLayer`, and `Export.image.toDrive`.

### 7.2. Local execution through the Earth Engine API

The Google Earth Engine Code Editor is not the only possible execution environment.

Satellite image acquisition and processing can also be performed programmatically through the official Earth Engine APIs, including the Python and JavaScript client libraries.

For local execution, users must configure the appropriate Earth Engine authentication and project settings.

The original scripts may require adaptation when transferred to a local environment, particularly for visualization and export operations that depend on Code Editor-specific functions.

Official documentation:

- [Earth Engine Python API](https://developers.google.com/earth-engine/guides/python_install)
- [Earth Engine JavaScript API](https://developers.google.com/earth-engine/guides/javascript)
- [Earth Engine Authentication](https://developers.google.com/earth-engine/guides/auth)

### 7.3. Reproducing the Python analysis without Google Earth Engine

**Access to Google Earth Engine is not required to reproduce the subsequent Python-based NDVI analysis and model simulations when the exported GeoTIFF datasets are used.**

The satellite imagery and associated research materials are publicly available through the project's Zenodo repository:

[https://doi.org/10.5281/zenodo.24237499](https://doi.org/10.5281/zenodo.24237499)

Researchers can download the required GeoTIFF files and execute the Python scripts locally, without accessing the Google Earth Engine Code Editor or performing the original satellite image acquisition again.

This allows the following procedures to be reproduced independently:

- Multispectral raster loading and processing.
- NDVI calculation.
- Descriptive statistical analysis.
- NDVI class distribution and area calculations.
- Comparative analysis between Recife and Fort Lauderdale.
- Empirical runoff modeling.
- Flood simulation and sensitivity analysis.

The Python execution requirements and instructions are described in the `scripts/README.md` and the main module documentation.

### 7.4. Reproducibility considerations

For reproducibility, the following aspects should be considered:

- The original JavaScript scripts are preserved in this directory.
- Image selection follows the `.first()` procedure implemented in each script.
- Cloud filtering and pixel-level masking differ between the study areas according to the original processing workflow.
- Sentinel-1 imagery is maintained separately from the optical NDVI processing workflow.
- Export commands are provided in the scripts but are commented out by default.
- The metadata of the GeoTIFF files used in the Python analysis should be consulted when identifying the actual input datasets.
- Exported raster files should be kept consistent with the filenames and paths expected by the Python processing scripts.

## 8. Related Documentation

For further information, refer to:

- [`../README.md`](../README.md) — Main documentation for the NDVI analysis module.
- [`../scripts/README.md`](../scripts/README.md) — Documentation of the Python processing and analysis scripts.

## 9. Data Sources and References

### Satellite data collections

- [Google Earth Engine](https://earthengine.google.com/)
- [Sentinel-2 Surface Reflectance Harmonized](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED)
- [Sentinel-1 SAR GRD](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD)

### Research dataset

Souza, A. F. L. M. (2026). *Americas TechGuard – NDVI Analysis Research Dataset*. Zenodo. https://doi.org/10.5281/zenodo.24237499

### Source code

[Americas TechGuard – NDVI Analysis](https://github.com/AntonioFernando/Americas_TechGuard/tree/main/modules/ndvi_analysis)
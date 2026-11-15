/*
 * Project: Americas TechGuard
 * Module: NDVI Analysis
 * Script: Sentinel-2 imagery acquisition for Fort Lauderdale, USA
 *
 * Dataset: COPERNICUS/S1_GRD
 * Study period: 2023
 * Spatial resolution: 10 m
 * Main bands: 'VV','VH'
 *
 * Purpose:
 * Retrieve and export Sentinel-2 imagery for
 * NDVI analysis and urban flood susceptibility assessment.
 */

var imageCollection = ee.ImageCollection("COPERNICUS/S1_GRD"),
    geometry =
    /* color: #d63000 */
    /* shown: false */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[-80.43917827812417, 26.17594120812011],
          [-80.43917827812417, 26.035357186875977],
          [-80.1164548894523, 26.035357186875977],
          [-80.1164548894523, 26.17594120812011]]], null, false);

var s1 = ee.ImageCollection('COPERNICUS/S1_GRD')
              .filterDate('2023-04-11', '2023-04-14')//flood date is 2023-04-12
               .filterBounds(geometry)
               .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
               .filter(ee.Filter.eq('instrumentMode', 'IW'));

var imagem = s1.first();

var bandas = imagem.clip(geometry);

var visParams = {min: -25, max: 0};

Map.setCenter(-80.23151529544502,26.125394171850775);

// Adicionar camadas VV e VH
Map.addLayer(bandas.select('VV'), visParams, 'VV');
Map.addLayer(bandas.select('VH'), visParams, 'VH');

print (s1)

// uncoment the block below to generate downloadable Geotiff file

// Export.image.toDrive({
//   image: bandas.select(['VV','VH']),
//   description: 'Fort_Lauderdale_SAR',
//   scale: 10,  // Sentinel-1 has 10m in IW
//   region: geometry,
//   maxPixels: 1e13
// });
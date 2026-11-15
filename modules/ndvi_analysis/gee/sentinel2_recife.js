/*
 * Project: Americas TechGuard
 * Module: NDVI Analysis
 * Script: Sentinel-2 imagery acquisition for Recife, Brazil
 *
 * Dataset: COPERNICUS/S2_SR_HARMONIZED
 * Study period: 2022
 * Spatial resolution: 10 m
 * Main bands: B4 (Red), B8 (NIR)
 *
 * Purpose:
 * Retrieve and export Sentinel-2 imagery for
 * NDVI analysis and urban flood susceptibility assessment.
 */

var imageCollection = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED"),
    geometry =
    /* color: #d63000 */
    /* shown: false */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[-35.00430348639094, -8.028274606057956],
          [-35.00430348639094, -8.093201369497764],
          [-34.85976460699641, -8.093201369497764],
          [-34.85976460699641, -8.028274606057956]]], null, false),
    imageCollection2 = ee.ImageCollection("LANDSAT/LC09/C02/T1_TOA"),
    imageCollection3 = ee.ImageCollection("LANDSAT/LC08/C02/T1_TOA"),
    imageCollection4 = ee.ImageCollection("COPERNICUS/S1_GRD");

function maskS2clouds(image) {
  var scl = image.select('SCL');
  var mask = scl.neq(3)   // cloud shadow
                .and(scl.neq(8))  // cloud medium probability
                .and(scl.neq(9))  // cloud high probability
                .and(scl.neq(10)) // thin cirrus
                .and(scl.neq(11)); // snow
  return image.updateMask(mask);
}

var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
              .filterDate('2022-08-01', '2022-08-30')
              .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',5))
              .filterBounds(geometry)
              .map(maskS2clouds);
              // .sort('CLOUDY_PIXEL_PERCENTAGE');

var landsat = ee.ImageCollection("LANDSAT/LC08/C02/T1_TOA")
               .filterDate('2022-07-01','2022-07-10')
               .filter(ee.Filter.lt('CLOUD_COVER',100))
               .filterBounds(geometry)
              // .sort('CLOUDY_PIXEL_PERCENTAGE');

var sar = ee.ImageCollection("COPERNICUS/S1_GRD")
               .filterDate('2022-02-27', '2022-04-30')
               .filterBounds(geometry)
               .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
               .filter(ee.Filter.eq('instrumentMode', 'IW'));


var imagem = s2.first();

var bandas = imagem.clip(geometry);

var bandas4e8 = imagem.select(['B8', 'B4']).clip(geometry);

var visParams = {min: -25, max: 0};

Map.setCenter(-35.00430348639094,-8.093201369497764);

Map.addLayer(bandas, {bands: ['B4', 'B3', 'B2'], min:500, max:3000}, 'bandas');

Map.addLayer(bandas4e8, {bands: ['B8', 'B4'], min:500, max:3000}, 'B4 e B8');

// Map.addLayer(bandas.select('VV'), visParams, 'VV');
// Map.addLayer(bandas.select('VH'), visParams, 'VH');

print (s2);

// Export.image.toDrive({
//   image: imagem
//             .select(['B8','B4','B3','B2'])
//             .clip(geometry),
//   description: 'Recife_MSI',
//   scale: 10,
//   region: geometry,
//   maxPixels: 1e13
// });

var imagem_uint16 = imagem.select(imagem.bandNames())
                          .toUint16();

// uncoment the block below to generate downloadable MSI Geotiff file

// Export.image.toDrive({
//   image: imagem_uint16.clip(geometry),
//   description: 'Recife_MSI_all_bands',
//   scale: 10,
//   region: geometry,
//   maxPixels: 1e13
// });

// uncoment the block below to generate downloadable SAR Geotiff file

// Export.image.toDrive({
//   image: bandas.select(['VV','VH']),  // selecionar polarizações que você quer
//   description: 'Recife_SAR',
//   scale: 10,  // Sentinel-1 tem 10m para modo IW
//   region: geometry,
//   maxPixels: 1e13
// });
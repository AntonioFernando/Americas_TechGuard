/*
 * Project: Americas TechGuard
 * Module: NDVI Analysis
 * Script: Sentinel-2 imagery acquisition for Fort Lauderdale, USA
 *
 * Dataset: COPERNICUS/S2_SR_HARMONIZED
 * Study period: 2023
 * Spatial resolution: 10 m
 * Main bands: B4 (Red), B8 (NIR)
 *
 * Purpose:
 * Retrieve and export Sentinel-2 imagery for
 * NDVI analysis and urban flood susceptibility assessment.
 */

var imageCollection = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED"),
    geometry =
    /* color: #ffff99 */
    /* shown: false */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[-80.42480600589424, 26.18493219748393],
          [-80.42480600589424, 26.03510483446497],
          [-80.11787546390205, 26.03510483446497],
          [-80.11787546390205, 26.18493219748393]]], null, false);

var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
               .filterDate('2023-03-03', '2023-03-16') // change date accordingly
               // after the flood ('2023-04-15') need to set clould percentage higher
               // during the flood ('2023-04-12') cloudy. use SAR script
               // before the flood ('2023-03-06')
               .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',5)) //for after flood image set the percentage to 50
               .filterBounds(geometry)
              // .sort('CLOUDY_PIXEL_PERCENTAGE');

var imagem = s2.first();

var bandas = imagem.clip(geometry);

var bandas4e8 = imagem.select(['B4', 'B8']).clip(geometry);

Map.setCenter(-80.23151529544502,26.125394171850775);

Map.addLayer(bandas, {bands: ['B4', 'B3', 'B2'], min:0, max:3000}, 'bandas');

Map.addLayer(bandas4e8, {bands: ['B4', 'B8'], min:0, max:3000}, 'B4 e B8');

print (s2);
  // uncoment the block below to generate downloadable Geotiff file
  
  // Export.image.toDrive({
  //   image: imagem
  //             .select(['B8','B4','B3','B2'])
  //             .clip(geometry),
  //   description: 'Fort_Lauderdale_MSI',
  //   scale: 10,
  //   region: geometry,
  //   maxPixels: 1e13
  // });

var imagem_uint16 = imagem.select(imagem.bandNames())
                          .toUint16();

// uncoment the block below to generate downloadable Geotiff file

// Export.image.toDrive({
//   image: imagem_uint16.clip(geometry),
//   description: 'Fort_Lauderdale_MSI_all_bands',
//   scale: 10,
//   region: geometry,
//   maxPixels: 1e13
// });
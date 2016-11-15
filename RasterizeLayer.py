# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 15:22:08 2016
https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html
https://pcjericks.github.io/py-gdalogr-cookbook/projection.html
@author: geoderek
"""

from osgeo import gdal, ogr

# Define pixel_size and NoData value of new raster
pixel_size = 5280
NoData_value = -9999

# Filename of input OGR file
vector_fn = 'C:/Data/PhD/Projects/NIJCrimeForcastingChallange/Data/NIJ2016_SEP01_SEP30.shp'

driver = ogr.GetDriverByName('ESRI Shapefile')
dataset = driver.Open(vector_fn)

# from Layer
layer = dataset.GetLayer()
spatialRef = layer.GetSpatialRef()
# from Geometry
feature = layer.GetNextFeature()
geom = feature.GetGeometryRef()
spatialRef = geom.GetSpatialReference()
print(spatialRef.ExportToWkt())



# Filename of the raster Tiff that will be created
raster_fn = 'C:/Data/PhD/Projects/NIJCrimeForcastingChallange/Data/test2.tif'

# Open the data source and read in the extent
source_ds = ogr.Open(vector_fn)
source_layer = source_ds.GetLayer()
x_min, x_max, y_min, y_max = source_layer.GetExtent()

# Create the destination data source
x_res = int((x_max - x_min) / pixel_size)
y_res = int((y_max - y_min) / pixel_size)
target_ds = gdal.GetDriverByName('GTiff').Create(raster_fn, x_res, y_res, 1, gdal.GDT_Byte)
target_ds.SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size))
band = target_ds.GetRasterBand(1)
band.SetNoDataValue(NoData_value)
target_ds.SetProjection(spatialRef.ExportToWkt())

# Rasterize
gdal.RasterizeLayer(target_ds, [1], source_layer, burn_values=[0])
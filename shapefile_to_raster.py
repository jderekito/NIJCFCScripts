# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 12:47:52 2016
Ref: https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html
@author: jmorgan3 
Step 1: Create raster based on extend of point shapefile
"""

from osgeo import gdal, ogr, osr
import os


#
# Please note that it will fail if a file with the same name already exists
try:
    os.remove(r'C:/Data/PhD/Projects/NIJCrimeForcastingChallange/Data/quadrats.tif')
except OSError:
    pass



# Define pixel_size and NoData value of new raster
pixel_size = 5280
NoData_value = -9999

# Filename of input OGR file
vector_fn = r'C:\Data\PhD\Projects\NIJCrimeForcastingChallange\Data\080116_083116_Data\NIJ2016_AUG01_AUG31.shp'

# Filename of the raster Tiff that will be created
raster_fn = 'C:/Data/PhD/Projects/NIJCrimeForcastingChallange/Data/quadrats.tif'

# Open the data source and read in the extent
source_ds = ogr.Open(vector_fn)
source_layer = source_ds.GetLayer()
x_min, x_max, y_min, y_max = source_layer.GetExtent()

#Build a buffer around the outward most features
#which will allow for them to not be on the edge
#x_min= x_min-pixel_size
#x_max= x_max+pixel_size
#y_min= y_min-pixel_size
#y_max= y_max+pixel_size

source_srs = source_layer.GetSpatialRef()

# Create the destination data source
x_res = int((x_max - x_min) / pixel_size)
y_res = int((y_max - y_min) / pixel_size)
target_ds = gdal.GetDriverByName('GTiff').Create(raster_fn, x_res, y_res, 1, gdal.GDT_Byte)
target_ds.SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size))
band = target_ds.GetRasterBand(1)
band.SetNoDataValue(NoData_value)
target_ds.SetProjection(source_srs.ExportToWkt())

print(source_srs)

# Rasterize
gdal.RasterizeLayer(target_ds, [1], source_layer, burn_values=[0])

    
print("done!")
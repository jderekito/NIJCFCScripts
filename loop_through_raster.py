# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 15:43:19 2016

@author: jmorgan3
"""

import gdal

#Set GeoTiff driver
driver = gdal.GetDriverByName("GTiff")
driver.Register()

#Open raster and read number of rows, columns, bands
dataset = gdal.Open("C:/Data/PhD/Projects/NIJCrimeForcastingChallange/Data/test_raster.tif")
cols = dataset.RasterXSize
rows = dataset.RasterYSize
allBands = dataset.RasterCount
band = dataset.GetRasterBand(1)

#Get array of raster cell values.  The two zeros tell the 
#iterator which cell to start on and the 'cols' and 'rows' 
#tell the iterator to iterate through all columns and all rows.
def get_raster_cells(band,cols,rows):
    return band.ReadAsArray(0,0,cols,rows)

#Bind array to a variable
rasterData = get_raster_cells(band,cols,rows)
#The array will look something like this if you print it
print(rasterData)

row_count = 1
for row in rasterData:
    print("vals for row:" + str(row_count))
    for val in row:
        print(val)
#        print(type(val))
    row_count = row_count+1
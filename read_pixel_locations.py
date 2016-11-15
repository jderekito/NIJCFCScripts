# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 22:24:19 2016
https://scriptndebug.wordpress.com/2014/11/24/latitudelongitude-of-each-pixel-using-python-and-gdal/
@author: geoderek
"""

from osgeo import gdal

# Open tif file
ds = gdal.Open("C:/Data/PhD/Projects/NIJCrimeForcastingChallange/Data/quadrats.tif")

xoff, a, b, yoff, d, e = ds.GetGeoTransform()

def pixel2coord(x, y):
    """Returns global coordinates from pixel x, y coords"""
    xp = a * x + b * y + xoff
    yp = d * x + e * y + yoff
    return(xp, yp)

# get columns and rows of your image from gdalinfo
cols = ds.RasterXSize+1
print(cols)
rows = ds.RasterYSize+1
print(rows)

row_ct = 0
col_ct = 0
if __name__ == "__main__":
    for row in  range(0,rows):
        row_ct = row_ct+1
#        print("row count: " + str(row_ct))
        for col in  range(0,cols): 
           x,y = pixel2coord(col,row)
           myList = [x,y]
           myList = ','.join(map(str, myList)) 
           print(myList)
           col_ct = col_ct+1
#           print("col count: " + str(col_ct))
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 22:21:57 2016

@author: jmorgan3
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 22:24:19 2016
https://scriptndebug.wordpress.com/2014/11/24/latitudelongitude-of-each-pixel-using-python-and-gdal/
@author: geoderek
Step 3: Create vector quadrats from raster
"""

from osgeo import gdal, ogr

# Open tif file
ds = gdal.Open("C:/Data/PhD/Projects/NIJCrimeForcastingChallange/Data/quadrats.tif")
pixel_size = 5280

xoff, a, b, yoff, d, e = ds.GetGeoTransform()

def pixel2coord(x, y):
    """Returns global coordinates from pixel x, y coords"""
    xp = a * x + b * y + xoff
    yp = d * x + e * y + yoff
    return(xp, yp)
    
# get columns and rows of your image from gdalinfo
cols = ds.RasterXSize+1
#print(cols)
rows = ds.RasterYSize+1
#print(rows)

row_ct = 0
col_ct = 0
if __name__ == "__main__":
    for row in  range(0,rows):
        row_ct = row_ct+1
        for col in  range(0,cols): 
            x,y = pixel2coord(col,row)
            # create a geometry from coordinates
            pt = ogr.Geometry(ogr.wkbPoint)
            pt.SetPoint_2D(0, x, y) # X, Y; in that order!
            buff = pt.Buffer(pixel_size/2)
            #create polygon object:
            (minX, maxX, minY, maxY) = buff.GetEnvelope()
            ring = ogr.Geometry(type=ogr.wkbLinearRing)
            ring = ogr.Geometry(ogr.wkbLinearRing)
            ring.AddPoint_2D(minX, minY)
            ring.AddPoint_2D(maxX, minY)
            ring.AddPoint_2D(maxX, maxY)
            ring.AddPoint_2D(minX, maxY)
            ring.AddPoint_2D(minX, minY)
            poly_envelope = ogr.Geometry(type=ogr.wkbPolygon)
            poly_envelope.AddGeometry(ring)        
            print('"'+str(poly_envelope.ExportToWkt()+'"'))
    
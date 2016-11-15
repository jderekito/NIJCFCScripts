# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 11:13:08 2016

@author: jmorgan3 TEST
"""

import ogr, csv, os


#
# Please note that it will fail if a file with the same name already exists
try:
    os.remove(r'C:/Data/PhD/Projects/NIJCrimeForcastingChallange/Data/poly_grid.shp')
except OSError:
    pass

# Filename of input OGR file
vector_fn = r'C:\Data\PhD\Projects\NIJCrimeForcastingChallange\Data\080116_083116_Data\party_aug.shp'
# Open the data source and read in the extent
source_ds = ogr.Open(vector_fn)
source_layer = source_ds.GetLayer()
source_srs = source_layer.GetSpatialRef()



driver = ogr.GetDriverByName("ESRI Shapefile")
dstfile = driver.CreateDataSource(r'C:/Data/PhD/Projects/NIJCrimeForcastingChallange/Data/poly_grid.shp') # Your output file


dstlayer = dstfile.CreateLayer("layer", source_srs, geom_type=ogr.wkbPolygon) 
#
## Add the other attribute fields needed with the following schema :
fielddef = ogr.FieldDefn("ID", ogr.OFTInteger)
fielddef.SetWidth(10)
dstlayer.CreateField(fielddef)
#
#fielddef = ogr.FieldDefn("Name", ogr.OFTString)
#fielddef.SetWidth(80)
#dstlayer.CreateField(fielddef)

# Read the feature in your csv file:
nb=1
with open(r'C:\Data\PhD\Projects\NIJCrimeForcastingChallange\Data\polys_wkt.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    print(reader)
    for row in reader: 
#        print(row['WKT'])
        poly = ogr.CreateGeometryFromWkt(row['WKT'])
        feature = ogr.Feature(dstlayer.GetLayerDefn())
        feature.SetGeometry(poly)
        feature.SetField("ID", nb) # A field with an unique id.
        feature.SetField("Name", "polygrid") # And a name (which is in the first field of my test file)
        dstlayer.CreateFeature(feature)
        nb=nb+1
    feature.Destroy()
    dstfile.Destroy()
print("done")
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 16:16:08 2016
Calculate Kernel Density of points shapefile dataset
@author: geoderek

Workflow:
    1. Create grid from event point locations
    2. Create layer for grid centroids
    3. Looping through the grid
        a) At each grid count the number of points within the search 
        b) Weight the value of each event point contribution by the distance from the grid quadrat centroid
        c) compute the kde for the grid quadrat
 
References:
    http://gdal.org/python/osgeo.ogr.Geometry-class.html
    https://youtu.be/PBZVTjmhl74       
"""
from osgeo import gdal, ogr, osr
import os, fiona, shapely.geometry
from shapely.geometry import Point

def shape_to_raster(vector_in, raster_out, pixel_size):
    try:
        os.remove(raster_out)
    except OSError:
        pass
    pixel_size = 1320 # Define NoData value of new raster
    NoData_value = -9999
    source_ds = ogr.Open(vector_in)
    source_layer = source_ds.GetLayer()
    x_min, x_max, y_min, y_max = source_layer.GetExtent()
    #Build a buffer around the outward most features
    #which will allow for them to not be on the edge
    x_min= x_min-pixel_size
    x_max= x_max+pixel_size
    y_min= y_min-pixel_size
    y_max= y_max+pixel_size
    source_srs = source_layer.GetSpatialRef()
    x_res = int((x_max - x_min) / pixel_size)
    y_res = int((y_max - y_min) / pixel_size)
    target_ds = gdal.GetDriverByName('GTiff').Create(raster_out, x_res, y_res, 1, gdal.GDT_Byte)
    target_ds.SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size))
    band = target_ds.GetRasterBand(1)
    band.SetNoDataValue(NoData_value)
    print(source_srs.ExportToWkt())
    target_ds.SetProjection(source_srs.ExportToWkt())
    gdal.RasterizeLayer(target_ds, [1], source_layer, burn_values=[0])
    print("Done w/ shape_to_raster!")

def raster_to_grid_centroids(raster_in):
    #need to revisit this because I am not getting the center point of the 
    #raster grid, but I am getting a regular spaced pattern which will work
    #http://osm.dumoulin63.net/osm2kml/
    ds = gdal.Open(raster_in)
    pixel_size = 1320
    cols = ds.RasterXSize+1
    rows = ds.RasterYSize+1
    row_ct = 0
    point_list = []
    if __name__ == "__main__":
        for row in  range(0,rows):
            row_ct = row_ct+1
            for col in  range(0,cols): 
                x,y = pixel2coord(col,row, ds)
                print(x,y)
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
                print(poly_envelope)
                centroid = poly_envelope.Centroid()
                #print('"'+str(centroid.ExportToWkt()+'"'))
                #print('"'+str(poly_envelope.ExportToWkt()+'"'))
                point_list.append(centroid.ExportToWkt())
#                print(centroid.ExportToWkt())
        return point_list
                

def pixel2coord(x, y, ds):
    """Returns global coordinates from pixel x, y coords"""
    xoff, a, b, yoff, d, e = ds.GetGeoTransform()
    xp = a * x + b * y + xoff
    yp = d * x + e * y + yoff
    return(xp, yp)

event_pts = r'C:\Data\PhD\Projects\NIJCrimeForcastingChallange\Data\080116_083116_Data\party_aug.shp'
raster_out = 'C:/Data/PhD/Projects/NIJCrimeForcastingChallange/Data/quadrats.tif'
raster_grid_size = 5280

#1. create raster from event points
shape_to_raster(event_pts, raster_out, raster_grid_size) 
#2. create list of centroids of that raster
poly_grid_wkt_list = raster_to_grid_centroids(raster_out)

#3. create a point shapefile of center points
# Please note that it will fail if a file with the same name already exists
try:
    os.remove(r'C:/Data/PhD/Projects/NIJCrimeForcastingChallange/Data/center_points.shp')
except OSError:
    pass
# Open the data source and read in the extent
source_ds = ogr.Open(event_pts)
source_layer = source_ds.GetLayer()
source_srs = source_layer.GetSpatialRef()
driver = ogr.GetDriverByName("ESRI Shapefile")
dstfile = driver.CreateDataSource(r'C:/Data/PhD/Projects/NIJCrimeForcastingChallange/Data/center_points.shp') # Your output file
dstlayer = dstfile.CreateLayer("layer", source_srs, geom_type=ogr.wkbPoint) 
## Add the other attribute fields needed with the following schema :
fielddef = ogr.FieldDefn("ID", ogr.OFTInteger)
fielddef.SetWidth(10)
dstlayer.CreateField(fielddef)
# Read the feature in your csv file:
nb=1
for gcp_wkt in poly_grid_wkt_list:
    pt = ogr.CreateGeometryFromWkt(gcp_wkt)
    feature = ogr.Feature(dstlayer.GetLayerDefn())
    feature.SetGeometry(pt)
    feature.SetField("ID", nb) # A field with an unique id.
    #feature.SetField("Name", "polygrid") # And a name (which is in the first field of my test file)
    dstlayer.CreateFeature(feature)
    nb=nb+1
feature.Destroy()
dstfile.Destroy()

#4. loop through grid center points and find the event points within a certain distance 

#Outer Loop through grid center points
#for feat in fiona.open(r'C:/Data/PhD/Projects/NIJCrimeForcastingChallange/Data/center_points.shp'):
#    print(feat)






#for gcp_wkt in poly_grid_wkt_list:
#    print(gcp_wkt)
#    gcp_geom = ogr.CreateGeometryFromWkt(gcp_wkt)
#    print(Point(0,0).geom_type)
    #Inner loop through event points to see if they are within search radius of gcp
#    for event_pt in fiona.open(event_pts):
#        event_pt_geom = shapely.geometry.shape(event_pt["geometry"])
#        distance_between_pts = gcp_geom.distance(event_pt_geom)
#        #print(distance_between_pts)
    

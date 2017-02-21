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
import os, fiona, shapely.geometry, math
from shapely.geometry import Point

def shape_to_raster(vector_in, raster_out, pixel_size):
    try:
        os.remove(raster_out)
    except OSError:
        pass
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
    cols = ds.RasterXSize+1
    rows = ds.RasterYSize+1
    row_ct = 0
    point_list = []
    if __name__ == "__main__":
        for row in  range(0,rows):
            row_ct = row_ct+1
            for col in  range(0,cols): 
                x,y = pixel2coord(col,row, ds)
                #print("POINT("+str(x)+" "+str(y)+")")
                point_list.append("POINT("+str(x)+" "+str(y)+")")
        return point_list
                

def pixel2coord(col, row, ds):
    c, a, b, f, d, e = ds.GetGeoTransform()
    """Returns global coordinates to pixel center using base-0 raster index"""
    xp = a * col + b * row + a * 0.5 + b * 0.5 + c
    yp = d * col + e * row + d * 0.5 + e * 0.5 + f
    return(xp, yp)

def create_center_points_shapefile(will_be_input):
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
    

    
    
event_pts = r'C:\Data\PhD\Projects\NIJCrimeForcastingChallange\Data\080116_083116_Data\street_crime_aug.shpp'
raster_out = 'C:/Data/PhD/Projects/NIJCrimeForcastingChallange/Data/quadrats.tif'
raster_grid_size = 330 #Specifically that the area of each cell is between 62,500 – 360,000 sq.ft.

#1. create raster from event points
#shape_to_raster(event_pts, raster_out, raster_grid_size) 
#2. create list of centroids of that raster
#poly_grid_wkt_list = raster_to_grid_centroids(raster_out)

#3. create a point shapefile of center points
# Please note that it will fail if a file with the same name already exists
#create_center_points_shapefile("test")

#4 compute kde
lhs = 3/(math.pi*math.pow(330,2))
print('lhs={0:.10f}'.format(lhs))

for center_pt_feature in fiona.open(r'C:/Data/PhD/Projects/NIJCrimeForcastingChallange/Data/center_points.shp'):
    center_pt_geom = shapely.geometry.shape(center_pt_feature["geometry"])
    buffer_result = center_pt_geom.buffer(330)
    rhs_sum=0.0
    lhs_x_rhs_sum=0.0
    with fiona.open(r'C:\Data\PhD\Projects\NIJCrimeForcastingChallange\Data\080116_083116_Data\street_crime_aug.shp') as event_pts:
        for event_pt_feature in event_pts:
            event_geom = shapely.geometry.shape(event_pt_feature["geometry"])
            #buffer method
            intersects_question = event_geom.within(buffer_result)
            #distance method is slower
            #intersects_question = center_pt_geom.distance(event_geom)<330
            if intersects_question:
                #print(center_pt_feature["id"]+" is near "+event_pt_feature["id"]+" with:")
                distance_between_pts = center_pt_geom.distance(event_geom)
                #print("d={:f}".format((330-distance_between_pts)/330))
                d=(330-distance_between_pts)/330
                rhs_sum=rhs_sum+d
                lhs_x_rhs_sum=lhs_x_rhs_sum+(lhs*d)
        if rhs_sum>0:
            #print("rhs_sum={:f}".format(rhs_sum))
            print("lhs_x_rhs_sum={:f}".format(lhs_x_rhs_sum))

print("DONE AND DONE!!!!!")

#4. loop through grid center points and find the the following:
    # 1. the number of event points within a certain distance, weighted by distance... aka kde
    #   2. the average distance to those points
    # 3. the number of street lights within a certain distance 
    #   4. the average distance to those street lights
    # 5. the number of street lines within a certain distance 
    #   6. the average distance to those street lines
        
        
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
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

Note: spatial indexes are very important for these type of workflows
A gouple of really good resources
http://gis.stackexchange.com/questions/119919/maximizing-code-performance-for-shapely
https://snorfalorpagus.net/blog/2014/05/12/using-rtree-spatial-indexing-with-ogr/
 
References:
    http://gdal.org/python/osgeo.ogr.Geometry-class.html
    https://youtu.be/PBZVTjmhl74 
      
"""
from osgeo import gdal, ogr, osr
import fiona, shapely.geometry
import rtree, os, math
from shapely.geometry import mapping

center_points_file = r'C:\Data\PhD\Projects\NIJCrimeForcastingChallange\Data\center_points_test.shp'
street_lines_file = r'C:\Data\PhD\Projects\NIJCrimeForcastingChallange\Data\street_crime_test.shp'

#center_points_file = r'C:\Data\PhD\Projects\NIJCrimeForcastingChallange\Data\center_points.shp'
#event_points_file = r'C:\Data\PhD\Projects\NIJCrimeForcastingChallange\Data\080116_083116_Data\street_crime_aug.shp'

os.chdir(r'C:\Data\PhD\Projects\NIJCrimeForcastingChallange\Data')


events_dictionary = {}
index = rtree.index.Index()
with fiona.open(street_lines_file, 'r') as event_points_layer:
    for event_point_feature in event_points_layer:
        event_point_geom = shapely.geometry.shape(event_point_feature['geometry'])
        event_point_geom_buffer = shapely.geometry.shape(event_point_feature['geometry']).buffer(165)
        events_dictionary[event_point_feature['id']] = event_point_geom
        index.insert(int(event_point_feature['id']), event_point_geom_buffer.bounds)
#print(events_dictionary)

with fiona.open(center_points_file, 'r') as center_points_layer:
    schema = center_points_layer.schema.copy()
    source_crs = center_points_layer.crs
    with fiona.open('center_points_kde_run.shp', 'w', 'ESRI Shapefile', schema, source_crs) as target:
        for center_point_feature in center_points_layer:
            fid = int(center_point_feature['id'])
            center_point_geom = shapely.geometry.shape(center_point_feature['geometry'])
            center_point_geom_buffer = shapely.geometry.shape(center_point_feature['geometry']).buffer(165)
            print('checking center point {}'.format(center_point_feature['id']))
            rhs_sum=0.0
            lhs_x_rhs_sum=0.0
            for j in index.intersection(center_point_geom_buffer.bounds):
                print('event {} within {} distance of center {}'.format(j, center_point_geom.distance(events_dictionary[str(j)]), center_point_feature['id']))
                distance_between_pts = center_point_geom.distance(events_dictionary[str(j)])
                if distance_between_pts<330:
                    d=(330-distance_between_pts)/330
                    rhs_sum=rhs_sum+d
                    lhs_x_rhs_sum=lhs_x_rhs_sum+(lhs*d)                
            center_point_feature['properties'] = {'kde': lhs_x_rhs_sum, 'ID': center_point_feature['id']}
            target.write({'properties':center_point_feature['properties'],'geometry': mapping(shapely.geometry.shape(center_point_feature['geometry']))})
print("DONE AND DONE!!!!!")


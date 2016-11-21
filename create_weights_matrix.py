# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 11:20:01 2016

@author: jmorgan3

hStep 4: Looping through polygrid, create distance weights matrix in csv format of: source,target,weight
http://rexdouglass.com/fast-spatial-joins-in-python-with-a-spatial-index/
Needed to install rtree http://www.lfd.uci.edu/~gohlke/pythonlibs/#rtree
pip install Rtree-0.8.2-cp35-cp35m-win_amd64.whl
"""

import shapefile
import shapely.geometry
from rtree import index
idx = index.Index()

#Load the shapefile of polygons and convert it to shapely polygon objects
polygons_sf = shapefile.Reader("C:/Data/PhD/Projects/NIJCrimeForcastingChallange/Data/poly_grid_clip_5mi.shp")
polygon_shapes = polygons_sf.shapes()
polygon_points = [q.points for q in polygon_shapes ]
from shapely.geometry import Polygon
polygons = [Polygon(q) for q in polygon_points]

#Build a spatial index based on the bounding boxes of the polygons
count = -1
for q in polygon_shapes:
    count +=1
    idx.insert(count, q.bbox)

count=0
from_wgt_array=[]
to_wgt_array=[]
for p_from in polygons:  
    print(str(count))
    from_wgt_array.append(False)
    for p_to in polygons:  
        print(p_from.touches(p_to))
        to_wgt_array.append(p_from.touches(p_to))
    count=count+1
print(from_wgt_array)
print(to_wgt_array)
    
    
    
    
    
    
##Load the shapefile of points and convert it to shapely point objects
#points_sf = shapefile.Reader("C:/Data/PhD/Projects/NIJCrimeForcastingChallange/Data/080116_083116_Data/car_cold_aug.shp")
#point_shapes = points_sf.shapes()
#from shapely.geometry import Point
#point_coords= [q.points[0] for q in point_shapes ]
#points = [Point(q.points[0]) for q in point_shapes ]
#    
#    
##Assign one or more matching polygons to each point
#matches = []
#for i in range(len(points)): #Iterate through each point
#    temp= None
#    print("Point ", i)
#    #Iterate only through the bounding boxes which contain the point
#    for j in idx.intersection( point_coords[i]):
#        #Verify that point is within the polygon itself not just the bounding box
#        if points[i].within(polygons[j]):
#            print("Match found! ",j)
#            temp=j
#            break
#    matches.append(temp) #Either the first match found, or None for no matches
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


#Load the shapefile of polygons and convert it to shapely polygon objects
polygons_sf = shapefile.Reader("C:/Data/PhD/Projects/NIJCrimeForcastingChallange/Data/poly_grid_clip_5mi.shp")
polygon_shapes = polygons_sf.shapes()
polygon_points = [q.points for q in polygon_shapes ]
from shapely.geometry import Polygon
polygons = [Polygon(q) for q in polygon_points]


count=1
from_wgt_array=[]
to_wgt_arrays=[]
for p_from in polygons:  
    #print(str(count))
    from_wgt_array.append(count)
    to_wgt_array=[]
    for p_to in polygons:  
        #print(p_from.touches(p_to))
        to_wgt_array.append(p_from.touches(p_to))
    to_wgt_arrays.append(to_wgt_array)
    count=count+1
#print(to_wgt_arrays)

#http://stackoverflow.com/questions/9535954/printing-lists-as-tabular-data
import pandas
import numpy as np
data = np.array(to_wgt_arrays)
pandas.DataFrame(data, from_wgt_array,from_wgt_array)    
print(pandas.DataFrame(data, from_wgt_array,from_wgt_array)*1)
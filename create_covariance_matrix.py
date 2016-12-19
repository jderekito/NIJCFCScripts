# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 17:13:46 2016
Create Covariance Matrix
Covariance is a measure of the degree to which the values for each data collection unit diviate from the arithmetic
mean for all units (Kimmerling et al. 2009)
@author: geoderek
"""

import fiona
import shapely.geometry

#1. Get mean of quadrat values
sum_dict = {}
for quadrat_feat in fiona.open("C:/Data/PhD/Projects/NIJCrimeForcastingChallange/Data/poly_grid_clip_5mi.shp"):
    print("quadrat_feat['id'] "+str(quadrat_feat['id']))
    quadrat_geom = shapely.geometry.shape(quadrat_feat["geometry"])
    pt_count=0
    with fiona.open(r"C:\Data\PhD\Projects\NIJCrimeForcastingChallange\Data\080116_083116_Data\party_aug.shp") as pts:
        for pt_feature in pts:
            pt_geom = shapely.geometry.shape(pt_feature["geometry"])
            point_within_quadrat = pt_geom.within(quadrat_geom)
            if point_within_quadrat:
                print(pt_geom)
                print(quadrat_geom)
                pt_count=pt_count+1
    print("pt_count :"+str(pt_count))
    sum_dict[int(quadrat_feat['id'])+1] = pt_count
print(sum_dict)

# Get sorted view of the keys.
sum_dict_sorted = sorted(sum_dict.keys())
running_sum=0
# Display the sorted keys.
for key in sum_dict_sorted:
    #print(key, sum_dict[key])
    running_sum=running_sum+sum_dict[key]
print("mean is: "+str(running_sum/len(sum_dict)))
mean=running_sum/len(sum_dict)

#2. Looping through each quadrat assign covariance
# using formula: cov=(i-mean)(j-mean)
from_cov_array=[]
to_cov_arrays=[]
count=1
for outter_key in sum_dict_sorted:
    #print(outter_key, sum_dict[outter_key])
    from_cov_array.append(count)
    inner_to_cov_arrays=[]
    for inner_key in sum_dict_sorted:
        cov=(sum_dict[outter_key]-mean)*(sum_dict[inner_key]-mean)
#        print(str(outter_key)+" to "+str(inner_key)+" to "+str(cov))
#        print("sum_dict[outter_key] "+str(sum_dict[outter_key]))
#        print("sum_dict[inner_key] "+str(sum_dict[inner_key]))
#        print("______")
        inner_to_cov_arrays.append(round(cov,2))
    to_cov_arrays.append(inner_to_cov_arrays)
    count=count+1
#print(from_cov_array)
#print(to_cov_arrays)
#for x in to_cov_arrays:
#    print(x)

#http://stackoverflow.com/questions/9535954/printing-lists-as-tabular-data
import pandas
import numpy as np
data = np.array(to_cov_arrays)
pandas.DataFrame(data, from_cov_array,from_cov_array)    
print(pandas.DataFrame(data, from_cov_array,from_cov_array)*1)


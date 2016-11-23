# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 09:45:30 2016
Count number of points-per-quadrat

@author: jmorgan3
"""

import fiona
import shapely.geometry

    
sum_dict = {}
for quadrat_feat in fiona.open("C:/Data/PhD/Projects/NIJCrimeForcastingChallange/Data/poly_grid_clip_5mi.shp"):
    #print(quadrat_feat['id'])
    quadrat_geom = shapely.geometry.shape(quadrat_feat["geometry"])
    pt_count=0
    with fiona.open(r"C:\Data\PhD\Projects\NIJCrimeForcastingChallange\Data\080116_083116_Data\party_aug.shp") as pts:
        for pt_feature in pts:
            pt_geom = shapely.geometry.shape(pt_feature["geometry"])
            point_within_quadrat = pt_geom.within(quadrat_geom)
            if point_within_quadrat:
                pt_count=pt_count+1
    sum_dict[quadrat_feat['id']] = pt_count
#print(sum_dict)

# Get sorted view of the keys.
sum_dict_sorted = sorted(sum_dict.keys())
# Display the sorted keys.
for key in sum_dict_sorted:
    print(key, sum_dict[key])
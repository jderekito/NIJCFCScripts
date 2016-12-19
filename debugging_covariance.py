# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 13:19:42 2016

@author: jmorgan3
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
#                print(pt_geom)
#                print(quadrat_geom)
                pt_count=pt_count+1
    print("pt_count :"+str(pt_count))
    sum_dict[int(quadrat_feat['id'])+1] = pt_count
print(sum_dict)
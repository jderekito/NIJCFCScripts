# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 20:04:07 2016
Calculate MVR
 @author: jmorgan3
"""
import fiona
import shapely.geometry


sum_dict = {}
for quadrat_feat in fiona.open("C:/Data/PhD/Projects/NIJCrimeForcastingChallange/Data/poly_grid_clip_5mi.shp"):
    #print(quadrat_feat['id'])
    quadrat_geom = shapely.geometry.shape(quadrat_feat["geometry"])
    pt_count=0
    with fiona.open(r"C:\Data\PhD\Projects\NIJCrimeForcastingChallange\Data\080116_083116_Data\illegal_dump_cold.shp") as pts:
        for pt_feature in pts:
            pt_geom = shapely.geometry.shape(pt_feature["geometry"])
            point_within_quadrat = pt_geom.within(quadrat_geom)
            if point_within_quadrat:
                pt_count=pt_count+1
    sum_dict[int(quadrat_feat['id'])+1] = pt_count
#print(sum_dict)

# Get sorted view of the keys.
sum_dict_sorted = sorted(sum_dict.keys())
running_sum=0
# Display the sorted keys.
for key in sum_dict_sorted:
    print(key, sum_dict[key])
    running_sum=running_sum+sum_dict[key]
print("mean is: "+str(running_sum/len(sum_dict)))
mean=running_sum/len(sum_dict)

running_deviation_sum=0
for key in sum_dict_sorted:
    #print(str(((sum_dict[key]-(running_sum/len(sum_dict)))**2)))
    running_deviation_sum=running_deviation_sum+((sum_dict[key]-(running_sum/len(sum_dict)))**2)

print("variance is: "+str(running_deviation_sum/len(sum_dict)))
variance=running_deviation_sum/len(sum_dict)
print("vmr is: "+str(variance/mean))


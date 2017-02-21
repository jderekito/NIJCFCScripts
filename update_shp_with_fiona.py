# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 10:28:45 2017
http://gis.stackexchange.com/questions/74858/fiona-preffered-method-for-defining-a-schema
http://toblerity.org/fiona/manual.html
@author: jmorgan3
"""
import shapely
from shapely.geometry import mapping
import fiona, os

os.chdir(r'C:\Data\PhD\Projects\NIJCrimeForcastingChallange\Data')

with fiona.open('test_fiona.shp', 'r') as source:
    schema = source.schema.copy()
    source_crs = source.crs
    with fiona.open('test_fiona_copy.shp', 'w', 'ESRI Shapefile', schema, source_crs) as target:
        for elem in source:
           elem['properties'] = {'Num': 1.45}
           target.write({'properties':elem['properties'],'geometry': mapping(shapely.geometry.shape(elem['geometry']))})
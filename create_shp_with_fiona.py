# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 10:21:04 2017

@author: jmorgan3
"""

import fiona
from fiona.crs import from_epsg
import os

os.chdir(r'C:\Data\PhD\Projects\NIJCrimeForcastingChallange\Data')
# schema of the shapefile
schema = {'geometry': 'Point', 'properties': {'Num' : 'float:9.6'}}
crs = from_epsg(7992)
with fiona.open('test_fiona.shp','w',driver='ESRI Shapefile', crs=crs,schema= schema) as output:
    geom = {'type': 'Point', 'coordinates': (5.0, 50.0)}
    prop = {'Num': 5.123456}
    output.write({'geometry':geom, 'properties': prop})
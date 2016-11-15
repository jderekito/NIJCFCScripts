# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 15:51:50 2016

@author: jmorgan3
Reference: https://pypi.python.org/pypi/pyshp
"""

import shapefile

sf = shapefile.Reader("C:/Data/PhD/Projects/NIJCrimeForcastingChallange/Data/NIJ2016_SEP01_SEP30.shp")
fields = sf.fields
print(fields)
geom = sf.shapes()

for feature in geom:
    # get each coord that makes up the polygon
    for coords in feature.points:
        x, y = coords[0], coords[1]
        print(x)
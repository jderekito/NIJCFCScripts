# -*- coding: utf-8 -*-
"""
References:
    http://toblerity.org/shapely/project.html

Pre-reqs software:
    download gdal, shapely & fiona from http://www.lfd.uci.edu/~gohlke/pythonlibs/
    at command prompt
    pip install Fiona-1.7.0-cp35-cp35m-win_amd64.whl
    pip install GDAL-2.0.3-cp35-cp35m-win_amd64.whl
    pip install Shapely-1.5.17-cp35-cp35m-win_amd64.whl

@author: jmorgan3
"""

import fiona
import shapely.geometry


for feat in fiona.open("C:/Data/PhD/Projects/NIJCrimeForcastingChallange/Data/NIJ2016_SEP01_SEP30.shp"):
    print(feat)
    start_pt_geom = shapely.geometry.shape(feat["geometry"])
    with fiona.open("C:/Data/PhD/Projects/NIJCrimeForcastingChallange/Data/NIJ2016_SEP01_SEP30.shp") as src:
        for feature in src:
            geom = shapely.geometry.shape(feature["geometry"])
            distance_between_pts = start_pt_geom.distance(geom)
            print(distance_between_pts)
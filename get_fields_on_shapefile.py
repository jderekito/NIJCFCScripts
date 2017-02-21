# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 10:04:37 2017

@author: jmorgan3
"""

from osgeo import ogr

daShapefile = r'C:\Data\PhD\Projects\NIJCrimeForcastingChallange\Data\test_fiona.shp'

dataSource = ogr.Open(daShapefile)
daLayer = dataSource.GetLayer(0)
layerDefinition = daLayer.GetLayerDefn()


print("Name  -  Type  Width  Precision")
for i in range(layerDefinition.GetFieldCount()):
    fieldName =  layerDefinition.GetFieldDefn(i).GetName()
    fieldTypeCode = layerDefinition.GetFieldDefn(i).GetType()
    fieldType = layerDefinition.GetFieldDefn(i).GetFieldTypeName(fieldTypeCode)
    fieldWidth = layerDefinition.GetFieldDefn(i).GetWidth()
    GetPrecision = layerDefinition.GetFieldDefn(i).GetPrecision()
    print(fieldName + " - " + fieldType+ " " + str(fieldWidth) + " " + str(GetPrecision))
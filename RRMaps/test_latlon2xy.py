#!/usr/bin/python
# -*- coding: utf-8 -*-

# from pyproj import Proj, transform
import pyproj
# from osgeo import osr
import math
import csv

# project_projection = pyproj.Proj(init="EPSG:4326")  # wgs84
# project_projection = pyproj.Proj("+init=EPSG:4326")
# google_projection = pyproj.Proj(init="EPSG:3857")  # default google projection

# longitude = -49.8170642
# latitude = -23.8819352

# step = 0.001

# final_long = -49.8000000
# final_lati = -23.8800000

# zoom = 10



# def LatLon2XY(Lat,Lon,Zoom,TileSize = 256):

TileSize = 256
Lat = -23.8819352
Lon = -49.8170642
Zoom = 10

NumberOfTiles = math.pow(2, Zoom)
X = (Lon+180)*(NumberOfTiles*TileSize)/360 #LonToX
Projection = math.log( math.tan( (math.pi/4) + math.radians(Lat/2) ) ) #LatToY
Y = Projection/math.pi

Y = 1-Y
# Y = (Y/2) * (NumberOfTiles*TileSize)
Y = Y/2 * (NumberOfTiles*TileSize)

X = X/256
Y = Y/256

print "X: {:d} Y: {:d} PROJ: {:f}".format(int(X),int(Y),Projection)


# def XY2LatLon(X,Y,Zoom,TileSize = 256):
NumberOfTiles = math.pow(2, Zoom)
X = X * TileSize
Y = Y * TileSize
Lon = (X*(360/(math.pow(2, Zoom)*TileSize)))-180;
Lat = Y*(2/(math.pow(2, Zoom)*TileSize))
Lat = 1-Lat
Lat = Lat * math.pi
Lat = math.degrees(math.atan(math.sinh(Lat)))

print "LAT: {:f} LON: {:f}".format(Lat,Lon)



# Coordinate displayToCoordinate(const QPoint& point, int zoom)
# {
#     // longitude
#     double longitude = (point.x()*(360/(pow(2,zoom)*256)))-180;
#     // latitude
#     double latitude = point.y()*(2/(pow(2,zoom)*256));
#     latitude = 1-latitude;
#     latitude = latitude*PI;
#     latitude = rad_deg(atan(sinh(latitude)));
    
#     Coordinate coord = Coordinate(longitude, latitude);
#     return coord;
# }

# print(x, y)
 
# p = pyproj.Proj("+proj=utm +zone=23K, +south +ellps=WGS84 +datum=WGS84 +units=m +no_defs") # use kwargs
# x,y = p(latitude, longitude)
# print 'x=%9.3f y=%11.3f' % (x,y)
# 
# from_srs = osr.SpatialReference()
# from_srs.ImportFromEPSG(4326)
# to_srs =  osr.SpatialReference()
# to_srs.ImportFromEPSG(3857)
# transf = osr.CoordinateTransformation(from_srs,to_srs)
# print transf.TransformPoint(longitude,latitude)
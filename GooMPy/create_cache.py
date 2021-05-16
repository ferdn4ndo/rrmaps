#!/usr/bin/env python
from goompy import GooMPy
from bs4 import BeautifulSoup

WIDTH = 600
HEIGHT = 600

LATITUDE  = -23.879908
LONGITUDE = -49.803486
START_ZOOM = 8
END_ZOOM = 22
ZOOM = 10
MAPTYPE = 'satellite'
KMLFILE = 'example.kml'

def main():
	for zoom in range(START_ZOOM,END_ZOOM):
		goompy = GooMPy(WIDTH, HEIGHT, LATITUDE, LONGITUDE, zoom, MAPTYPE, None, 4, 1, KMLFILE)
		goompy._KML2XY();
		goompy._fetch()



if __name__ == "__main__":
	main()
#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import math
import glob
from download_tiles import download_tiles
from merge_tiles import merge_tiles
from gmap_utils import *
import csv
import sys
import urllib2
import time
import random
import PIL.ImageDraw as ImageDraw,PIL.Image as Image, PIL.ImageShow as ImageShow 
# from PIL import Image
from bs4 import BeautifulSoup
from pprint import pprint


def main():
	zoom = 15

	lat_start, lon_start = -22.7994, -50.2373
	lat_stop, lon_stop = -22.7723, -50.1924

	last_xy = [0,0]
	line_points = []
	station_points = []
	xy = []
	tmp_folder = 'tmp/'
	user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1'
	headers = { 'User-Agent' : user_agent }

	#Delete previus temp
		
	# download_tiles(zoom, lat_start, lat_stop, lon_start, lon_stop, satellite=True, folder=temp_folder)
 
	# merge_tiles(zoom, lat_start, lat_stop, lon_start, lon_stop, satellite=True, folder=temp_folder)

	print "Reading KML..."
	with open('example.kml', 'r') as f:
		s = BeautifulSoup(f, 'xml')   
		lines = []
		for data in s.find_all('Placemark'):
			# print data
			line_points = []
			for coords in data.find_all('coordinates'):
				space_splits =  coords.string.encode("utf-8").replace(" ", "").split("\n")
				del space_splits[0]
				del space_splits[-1]
				count_splits = len(space_splits)
				name = 0
				if(count_splits==1): #station
					name = data.encode("utf-8").replace("</","").split("name>")[1]
					comma_split = space_splits[0].split(',')
					comma_split[2] = name
					station_points.append([comma_split[1],comma_split[0],comma_split[2]])
					actual_xy = latlon2xy(zoom, comma_split[1], comma_split[0])
					actual_px = latlon2px(zoom, comma_split[1], comma_split[0])
					lat_prop = actual_px[0]/256 - actual_xy[0]
					lon_prop = actual_px[1]/256 - actual_xy[1]
					if (lat_prop > 0.75): xy.append((actual_xy[0] + 1, actual_xy[1]))
					if (lat_prop < 0.25): xy.append((actual_xy[0] - 1, actual_xy[1]))
					if (lon_prop > 0.75): xy.append((actual_xy[0], actual_xy[1] + 1))
					if (lon_prop < 0.25): xy.append((actual_xy[0], actual_xy[1] - 1))
				else:
					sep_count = 2
					count = 0
					for split in space_splits[1:]:
						comma_split = split.split(',')
						comma_split[2] = name
						actual_xy = latlon2xy(zoom, comma_split[1], comma_split[0])
						actual_px = latlon2px(zoom, comma_split[1], comma_split[0])
						lat_prop = actual_px[0]/256 - actual_xy[0]
						lon_prop = actual_px[1]/256 - actual_xy[1]
						if (lat_prop > 0.75): xy.append((actual_xy[0] + 1, actual_xy[1]))
						if (lat_prop < 0.25): xy.append((actual_xy[0] - 1, actual_xy[1]))
						if (lon_prop > 0.75): xy.append((actual_xy[0], actual_xy[1] + 1))
						if (lon_prop < 0.25): xy.append((actual_xy[0], actual_xy[1] - 1))

						# print name
						line_points.append([comma_split[1],comma_split[0]])
						# if(abs(last_xy[0]-actual_xy[0])>0 or abs(last_xy[1]-actual_xy[1])>0):
						xy.append(actual_xy)
						# last_xy = actual_xy

			if (len(line_points)>0) :
				lines.append(line_points)

	print "Total XY points: ",len(xy)
	xy = f7(xy) #remove duplicates
	xy.sort() #ascending order
	print "Total unique XY points: ",len(xy)


	# Define sizes and create final image handler
	x_min = min(xy, key = lambda t: t[0])[0]
	x_max = max(xy, key = lambda t: t[0])[0]
	y_min = min(xy, key = lambda t: t[1])[1]
	y_max = max(xy, key = lambda t: t[1])[1]
	total_x = int((x_max - x_min)*256)
	total_y = int((y_max - y_min)*256)
	print "xmin:",x_min
	print "xmax:",x_max
	print "ymin:",y_min
	print "ymax:",y_max
	print "Totalx:",total_x
	print "Totaly:",total_y
	raw_input("Press Enter to continue...")
	result = Image.new("RGBA", (total_x, total_y))
	
	# Add every tile
	for coord in xy:
		print "Downloading coordenates: ",coord

		x = coord[0]
		y = coord[1]
		lyrs = 's' #h = roads only, m = standard roadmap, p = terrain, r = somehow altered roadmap, s = satellite only, t = terrain only, y = hybrid

		url = "https://mt0.google.com/vt/lyrs=%s&?x=%d&s=&y=%d&z=%d" % (lyrs, x, y, zoom)

		if not(os.path.isdir(tmp_folder)):
			os.mkdir(tmp_folder, 0755 );

		filename = tmp_folder+"%d_%d_%d_%s.jpg" % (zoom, x, y, lyrs)

		if not os.path.exists(filename):
			bytes = None
			try:
				req = urllib2.Request(url, data=None, headers=headers)
				response = urllib2.urlopen(req)
				bytes = response.read()
			except Exception, e:
				print "--", filename, "->", e
				sys.exit(1)

			if bytes.startswith("<html>"):
				print "-- forbidden", filename
				sys.exit(1)

			print "-- saving", filename

			f = open(filename,'wb')
			f.write(bytes)
			f.close()
			time.sleep(1 + random.random())

		i = Image.open(filename)
		x_paste = (x - x_min - 1) * 256
		y_paste = total_y - ((y_max - y) * 256)
		result.paste(i, (x_paste, y_paste))

		del i

	# Add every line point and then every station point
	draw = ImageDraw.Draw(result)
	station_size = 2;
	for line_points in lines:
		prev_line_x = 0
		prev_line_y = 0
		for point_ll in line_points:
			point_px = latlon2px(zoom,point_ll[0],point_ll[1])
			point_xy = latlon2xy(zoom,point_ll[0],point_ll[1])
			real_xy = [((point_px[0]/256) - x_min - 1)*256, total_y - ((y_max - (point_px[1]/256)) * 256)]
			if((prev_line_x!=0) or (prev_line_y!=0)):
				draw.line([(prev_line_x, prev_line_y),(real_xy[0], real_xy[1])],'white')
			prev_line_x = real_xy[0]
			prev_line_y = real_xy[1]
	for station_ll in station_points:
		station_px = latlon2px(zoom,station_ll[0],station_ll[1])
		station_xy = latlon2xy(zoom,station_ll[0],station_ll[1])
		real_xy = [((station_px[0]/256) - x_min - 1)*256, total_y - ((y_max - (station_px[1]/256)) * 256)]
		print "Station: ", real_xy
		draw.rectangle([real_xy[0]-station_size,real_xy[1]-station_size,real_xy[0]+station_size,real_xy[1]+station_size],fill='red')



	
	#Save and finish

	result.save("map_teste.jpg")

if __name__ == "__main__":
	main()
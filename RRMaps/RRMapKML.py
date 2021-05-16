#!/usr/bin/python
# -*- coding: utf-8 -*-
##
## KMLProcessing
##
import math
# from RRMapDownload import DownloadTiles
from bs4 import BeautifulSoup

class RRMapKML():

	def __init__(self, KMLFileName = ""):

		self.KMLFileName = KMLFileName
		self.LinePoints = []
		self.Lines = []
		self.StationPoints = []
		self.XY = []

		if(KMLFileName!=""):
			self.LoadKML()

	def SetKMLFileName(self, KMLFileName):
		self.KMLFileName = KMLFileName


	def LoadKML(self):
		print "Reading KML..."
		with open(self.KMLFileName, 'r') as f:
			s = BeautifulSoup(f, 'xml')   
			self.Lines = []
			for data in s.find_all('Placemark'):
				# print data
				self.LinePoints = []
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
						self.StationPoints.append([comma_split[1],comma_split[0],comma_split[2]])
						# actual_xy = latlon2xy(zoom, comma_split[1], comma_split[0])
						# actual_px = latlon2px(zoom, comma_split[1], comma_split[0])
						# lat_prop = actual_px[0]/256 - actual_xy[0]
						# lon_prop = actual_px[1]/256 - actual_xy[1]
						# if (lat_prop > 0.75): self.XY.append((actual_xy[0] + 1, actual_xy[1]))
						# if (lat_prop < 0.25): self.XY.append((actual_xy[0] - 1, actual_xy[1]))
						# if (lon_prop > 0.75): self.XY.append((actual_xy[0], actual_xy[1] + 1))
						# if (lon_prop < 0.25): self.XY.append((actual_xy[0], actual_xy[1] - 1))
					else:
						# sep_count = 2
						# count = 0
						for split in space_splits[1:]:
							comma_split = split.split(',')
							# comma_split[2] = name
							# actual_xy = latlon2xy(zoom, comma_split[1], comma_split[0])
							# actual_px = latlon2px(zoom, comma_split[1], comma_split[0])
							# lat_prop = actual_px[0]/256 - actual_xy[0]
							# lon_prop = actual_px[1]/256 - actual_xy[1]
							# if (lat_prop > 0.75): self.XY.append((actual_xy[0] + 1, actual_xy[1]))
							# if (lat_prop < 0.25): self.XY.append((actual_xy[0] - 1, actual_xy[1]))
							# if (lon_prop > 0.75): self.XY.append((actual_xy[0], actual_xy[1] + 1))
							# if (lon_prop < 0.25): self.XY.append((actual_xy[0], actual_xy[1] - 1))

							# print name
							self.LinePoints.append([comma_split[1],comma_split[0]])
							# if(abs(last_xy[0]-actual_xy[0])>0 or abs(last_xy[1]-actual_xy[1])>0):
							# self.XY.append(actual_xy)
							# last_xy = actual_xy

				if (len(self.LinePoints)>0) :
					self.Lines.append(self.LinePoints)

		# print "Total XY points: ",len(self.XY)
		# self.XY = DupeClean(self.XY) #remove duplicates
		# self.XY.sort() #ascending order
		# print "Total unique XY points: ",len(self.XY)
		pass

	def GetLines(self):
		return self.Lines

	# def GetLinePoints(self):
	# 	return self.LinePoints

	def GetStations(self):
		return self.StationPoints

	def DupeClean(self,seq):
		seen = set()
		seen_add = seen.add
		return [x for x in seq if not (x in seen or seen_add(x))]
#!/usr/bin/python
# -*- coding: utf-8 -*-
##
## Window image generation
##
from __future__ import unicode_literals
import math
# from RRMapDownload import DownloadTiles
from RRMapKML import RRMapKML
from RRMapDownload import RRMapDownload
from PIL import Image, ImageDraw, ImageFont
from multiprocessing import Pool

# class myThread (threading.Thread):
# 	def __init__(self, threadID, name, counter):
# 		threading.Thread.__init__(self)
# 		self.threadID = threadID
# 		self.name = name
# 		self.counter = counter
		
# 	def run(self):
# 		print "Starting " + self.name
# 		print_time(self.name, self.counter, 5)
# 		print "Exiting " + self.name

# 	def print_time(threadName, counter, delay):
# 		while counter:
# 			if exitFlag:
# 				threadName.exit()
# 			time.sleep(delay)
# 			print "%s: %s" % (threadName, time.ctime(time.time()))
# 			counter -= 1

# # Create new threads
# thread1 = myThread(1, "Thread-1", 1)
# thread2 = myThread(2, "Thread-2", 2)

# # Start new Threads
# thread1.start()
# thread2.start()

# print "Exiting Main Thread"

class RRMapImage():

	def __init__(self, WinWidth, WinHeight, CenterLat, CenterLon, Zoom, MapType = 'satellite', KMLFile = '', TileSize = 256, BackColor = 'white', TopBar = 1, TopBarH = 30):

		self.TileSize = TileSize
		self.MapType = self.getLyrs(MapType)
		self.Zoom = Zoom
		self.BackColor = BackColor
		self.TopBar = TopBar
		self.TopBarH = TopBarH

		self.LinePoints = []
		self.Lines = []
		self.Stations = []

		self.MapKML = RRMapKML(KMLFile)
		self.MapDownload = RRMapDownload()

		(self.WinWidth, self.WinHeight) = (WinWidth, WinHeight)

		self.SetSizes(CenterLat,CenterLon)

		self.GenerateImg()

	def SetSizes(self,CenterLat,CenterLon):
		CenterLat = float(CenterLat)
		CenterLon = float(CenterLon)
		(self.CenterLat,self.CenterLon) = (CenterLat,CenterLon)
		(self.CenterMapPixelX,self.CenterMapPixelY) = self.LatLon2Px(self.Zoom,CenterLat,CenterLon)
		(self.CenterMapX,self.CenterMapY) = self.LatLon2XY(self.Zoom,CenterLat,CenterLon)
		
		#Calculates the northeast corner
		CornerNEx = float(self.CenterMapPixelX)/self.TileSize - (self.WinWidth/2.0)/self.TileSize
		CornerNEy = float(self.CenterMapPixelY)/self.TileSize - (self.WinHeight/2.0)/self.TileSize
		self.CornerNE = (CornerNEx,CornerNEy)

		#Calculates the southwest corner
		CornerSWx = CornerNEx+(float(self.WinWidth)/self.TileSize)
		CornerSWy = CornerNEy+(float(self.WinHeight)/self.TileSize)
		self.CornerSW = (CornerSWx,CornerSWy)

		# print self.WinWidth/2
		print "Corner NE: ",self.CornerNE
		print "Corner SW: ",self.CornerSW
		
		self.TileImgX = (self.WinWidth/2)-((float(self.CenterMapPixelX)/self.TileSize)-self.CenterMapX)*self.TileSize
		self.TileImgY = (self.WinHeight/2)-((float(self.CenterMapPixelY)/self.TileSize)-self.CenterMapY)*self.TileSize

	def SetMapKML(self,KMLFile):
		self.KMLFile = KMLFile
		self.MapKML.SetKMLFileName(KMLFile)
		self.MapKML.LoadKML()

		self.Lines = self.MapKML.GetLines()
		self.Stations = self.MapKML.GetStations()

		CenterStation = self.Stations[0]

		self.SetSizes(CenterStation[0],CenterStation[1])

	def SetZoom(self,zoom):
		if zoom > 0 and zoom < 22:
			self.Zoom = zoom

	def SetMapLyrs(self,lyrs):
		self.MapType = lyrs

	def GenerateImg(self,width=0,height=0):
		if(width==0) and (height==0):
			width = self.WinWidth
			height = self.WinHeight
		else:
			self.WinWidth = width
			self.WinHeight = height
		Img = Image.new("RGB", (width, height), self.BackColor)

		(LastScreenX,LastScreenY) = (self.TileImgX, self.TileImgY)

		#ToDo: calculate new CenterMapX and CenterMapY based on scale of redraw on line 100/101 (now i'm 106)

		(TileNumberX,TileNumberY) = (self.CenterMapX, self.CenterMapY)

		TilesX = []
		NumberX = []
		NumberY = []

		ScreenX = self.TileImgX
		ScreenY = self.TileImgY

		# 1 - Find X begin
		while LastScreenX > 0:
			LastScreenX -= self.TileSize
			TileNumberX -= 1
			# self.DrawMapXYBox(Img, LastScreenX, LastScreenY, TileNumberX, TileNumberY)
			self.DrawMapXY(Img,LastScreenX,LastScreenY,TileNumberX,TileNumberY)
			TilesX.insert(0, LastScreenX)
			NumberX.insert(0, TileNumberX)

		# 2 - Find X end
		LastScreenX = self.TileImgX
		TileNumberX = self.CenterMapX
		while LastScreenX < width:
			# self.DrawMapXYBox(Img, LastScreenX, LastScreenY, TileNumberX, TileNumberY)
			self.DrawMapXY(Img,LastScreenX,LastScreenY,TileNumberX,TileNumberY)
			TilesX.insert(0, LastScreenX)
			NumberX.insert(0, TileNumberX)
			LastScreenX += self.TileSize
			TileNumberX += 1

		# 3 - Higher lines
		while LastScreenY > 0:
			LastScreenY -= self.TileSize
			TileNumberY -= 1
			NumberY.insert(0, TileNumberY)
			for Index, ScreenX in enumerate(TilesX):
				# self.DrawMapXYBox(Img, ScreenX, LastScreenY, NumberX[Index], TileNumberY)
				self.DrawMapXY(Img,ScreenX,LastScreenY,NumberX[Index],TileNumberY)

		# 4 - Lower lines
		LastScreenY = self.TileImgY + self.TileSize
		TileNumberY = self.CenterMapY + 1
		while LastScreenY < height:
			for Index, ScreenX in enumerate(TilesX):
				# self.DrawMapXYBox(Img, ScreenX, LastScreenY, NumberX[Index], TileNumberY)
				self.DrawMapXY(Img,ScreenX,LastScreenY,NumberX[Index],TileNumberY)
			LastScreenY += self.TileSize
			TileNumberY += 1
			NumberY.insert(0, TileNumberY)

		self.DrawCenterMarker(Img,width,height)

		# KML Layer
		MinX, MinY = self.CornerNE
		MaxX, MaxY = self.CornerSW
		KMLImg = self.GenerateKMLImg(width,height,MinX,MinY,MaxX,MaxY)
		Img.paste(KMLImg,mask=KMLImg)

		# 5 - Top Bar
		PDrawImg = Image.new('RGBA', (width, self.TopBarH))
		PDraw = ImageDraw.Draw(PDrawImg)
		PDraw.polygon([(0,0),(width,0),(width,self.TopBarH),(0,self.TopBarH)],
              fill=(0,0,0,172),outline=(0,0,0,128))
		self.DrawText(PDrawImg,'Map:',10,7)
		self.DrawText(PDrawImg,'Maker:',width-450,7)
		self.DrawText(PDrawImg,'Type:',width-250,7)
		self.DrawText(PDrawImg,'Zoom:',width-100,7)
		Img.paste(PDrawImg,mask=PDrawImg)

		# 6 - Status bar
		StatusHeight = 20
		StatusWidth = 220
		SDrawImg = Image.new('RGBA', (StatusWidth, StatusHeight))
		SDraw = ImageDraw.Draw(SDrawImg)
		SDraw.polygon([(0,0),(StatusWidth,0),(StatusWidth,StatusHeight),(0,StatusHeight)],
              fill=(0,0,0,172),outline=(0,0,0,128))
		self.DrawText(SDrawImg,'X: {:06.3f} Y: {:06.3f} Z: {:d} T: {:s}'.format(self.CenterMapPixelX/256,self.CenterMapPixelY/256,self.Zoom,self.MapType),5,2,12)
		Img.paste(SDrawImg,box=(0,height-StatusHeight),mask=SDrawImg)		
		
		# Img.show()
		return Img

	def GenerateKMLImg(self,width,height,minTileX,minTileY,maxTileX,maxTileY):
		KMLImg = Image.new('RGBA', (width, height))
		ElegibleStationPoints = []
		ElegibleLines = []

		for Station in self.Stations:
			#['-23.7497611', '-49.8307121', 'Barbosas']
			STLat = float(Station[0])
			STLon = float(Station[1])
			STTxt = Station[2].decode('utf-8')
			# STTxt = u'STTxt'

			STX,STY = self.LatLon2Px(self.Zoom,STLat,STLon)

			STX,STY = STX/self.TileSize, STY/self.TileSize

			# print STX,STY

			if (STX<maxTileX) and (STX>minTileX) and (STY<maxTileY) and (STY>minTileY):
				realSTX = (float(self.WinWidth)/2) - ((float(self.CenterMapPixelX)/self.TileSize)-STX)*self.TileSize
				realSTY = (float(self.WinHeight)/2) - ((float(self.CenterMapPixelY)/self.TileSize)-STY)*self.TileSize

				# print "Station: ", (realSTX,realSTY)
				self.DrawText(KMLImg,STTxt,realSTX,realSTY)

				# draw.rectangle([real_xy[0]-station_size,real_xy[1]-station_size,real_xy[0]+station_size,real_xy[1]+station_size],fill='red')


		# print width,height,minTileX,minTileY,maxTileX,maxTileY
		# print self.Stations
		# pass

		return KMLImg

	def DrawStation(self, STTxt, STX, )


	def DrawCenterMarker(self, Img, Width, Height, MarkerSizePx = 20):
		draw = ImageDraw.Draw(Img)
		Size = MarkerSizePx/2
		(CenterX, CenterY) = (round(Width/2),round(Height/2))
		draw.line([CenterX - Size, CenterY, CenterX + Size, CenterY], fill=(255,0,0)) #CROSSHAIR HOR
		draw.line([CenterX, CenterY - Size, CenterX, CenterY + Size], fill=(0,0,255)) #CROSSHAIR VER
		del draw

	def DrawMapXYCallback(self, Img, TileX, TileY, NumberX, NumberY, Zoom):
		# TileImg = self.MapDownload.DownloadXYZ(NumberX, NumberY, Zoom, self.MapType)
		Img.paste(TileImg,box=(TileX,TileY))
		return 0

	def DrawMapXY(self, Img, TileX, TileY, NumberX, NumberY, Zoom = 0):

		Zoom = self.Zoom if Zoom == 0 else Zoom

		TileX = int(TileX)
		TileY = int(TileY)

		# pool = Pool(processes=1) 
		# result = pool.apply_async(self.MapDownload.DownloadXYZ, [NumberX, NumberY, Zoom, self.MapType], self.DrawMapXYCallback) # Evaluate "f(10)" asynchronously calling callback when finished.

		TileImg = self.MapDownload.DownloadXYZ(NumberX, NumberY, Zoom, self.MapType)
		Img.paste(TileImg,box=(TileX,TileY))


	def DrawMapXYBox(self, Img, TileX, TileY, NumberX, NumberY):
		TextColor = (0,0,0)
		BoxColor = (64,64,64)
		FontName = 'Roboto-Bold.ttf'
		FontSize = 14
		Padding = 10
		BorderSize = 1

		TileSize = self.TileSize
		draw = ImageDraw.Draw(Img)
		draw.line([TileX, TileY, TileX + TileSize, TileY], fill=BoxColor) #BOX UPPER
		draw.line([TileX, TileY, TileX, TileY + TileSize], fill=BoxColor) #BOX LEFT
		draw.line([TileX + TileSize, TileY, TileX + TileSize, TileY + TileSize], fill=BoxColor) #BOX RIGHT 
		draw.line([TileX, TileY + TileSize, TileX + TileSize, TileY + TileSize], fill=BoxColor) #BOX BOTTOM
		del draw

		TileTitle = "({},{})".format(NumberX,NumberY)
		TileX = TileX if TileX >= 0 else 0
		TileY = TileY if TileY >= 0 else 0


		self.DrawText(Img, TileTitle, TileX + Padding, TileY + Padding)

	def DrawText(self, Img, Text, TextX, TextY, FontSize = 14, BorderSize = 1, TextColor = (255,255,255), BorderColor = (0,0,0), FontName = 'fonts/Roboto-Bold.ttf'):
		Font = ImageFont.truetype(FontName, FontSize)
		Draw = ImageDraw.Draw(Img)

		#Draw border
		if(BorderSize>0):
			Draw.text((TextX-BorderSize,TextY-BorderSize), Text, font=Font, fill=BorderColor)
			Draw.text((TextX-BorderSize,TextY+BorderSize), Text, font=Font, fill=BorderColor)
			Draw.text((TextX+BorderSize,TextY-BorderSize), Text, font=Font, fill=BorderColor)
			Draw.text((TextX+BorderSize,TextY+BorderSize), Text, font=Font, fill=BorderColor)


		#Draw center text
		Draw.text((TextX,TextY), Text, font=Font, fill=TextColor)
		del Draw


	def MoveXY(self, dx, dy):

		#ThanksTo: 
		#https://forum.openstreetmap.org/viewtopic.php?id=244
		#https://gis.stackexchange.com/questions/48949/epsg-3857-or-4326-for-googlemaps-openstreetmap-and-leaflet
		#https://gis.stackexchange.com/questions/133205/wmts-convert-geolocation-lat-long-to-tile-index-at-a-given-zoom-level

		CurrentX,CurrentY = self.LatLon2Px(self.Zoom,self.CenterLat,self.CenterLon)

		# k = .107*self.Zoom #Scaling factor
		k = .005*self.Zoom + 1 #Scaling factor

		NewX,NewY = CurrentX+dx*k, CurrentY+dy*k

		# print "dx: {:d} dy: {:d} OldX: {:f} OldY: {:f} NewX: {:f} NewY {:f}".format(dx,dy,CurrentX,CurrentY,NewX,NewY)

		CenterLat,CenterLon = self.XY2LatLon(self.Zoom,CurrentX+dx*k,CurrentY+dy*k)

		self.SetSizes(CenterLat,CenterLon)

		(self.CenterMapPixelX,self.CenterMapPixelY) = self.LatLon2Px(self.Zoom,self.CenterLat,self.CenterLon)
		(self.CenterMapX,self.CenterMapY) = self.LatLon2XY(self.Zoom,self.CenterLat,self.CenterLon)
		
		self.TileImgX = (self.WinWidth/2)-((float(self.CenterMapPixelX)/self.TileSize)-self.CenterMapX)*self.TileSize
		self.TileImgY = (self.WinHeight/2)-((float(self.CenterMapPixelY)/self.TileSize)-self.CenterMapY)*self.TileSize

	def LatLon2Px(self,Zoom,Lat,Lon,TileSize = 256):
		# print "LatLon2Px (Z:{:d},LAT:{:f},LON:{:f})".format(int(Zoom),Lat,Lon)
		NumberOfTiles = math.pow(2, Zoom)
		X = (Lon+180)*(NumberOfTiles*TileSize)/360 #LonToX
		Projection = math.log( math.tan( (math.pi/4) + math.radians(Lat/2) ) ) #LatToY
		Y = Projection/math.pi

		Y = 1-Y
		Y = Y/2 * (NumberOfTiles*TileSize)

		# print "Px: {:d} Py: {:d} PROJ: {:f}".format(int(X),int(Y),Projection)
		return X,Y

	def LatLon2XY(self,Zoom,Lat,Lon,TileSize = 256):
		# print "LatLon2XY (Z:{:d},LAT:{:f},LON:{:f})".format(int(Zoom),Lat,Lon)
		X,Y = self.LatLon2Px(Zoom,Lat,Lon,TileSize)
		# print "Px: {:d} Py: {:d}".format(int(X),int(Y))
		X = int(round(X/256))
		Y = int(round(Y/256))
		# print "X: {:d} Y: {:d}".format(X,Y)
		return X,Y

	def XY2LatLon(self,Zoom,X,Y,TileSize = 256):
		NumberOfTiles = math.pow(2, Zoom)
		# X = X * TileSize
		# Y = Y * TileSize
		Lon = (X*(360/(math.pow(2, Zoom)*TileSize)))-180;
		Lat = Y*(2/(math.pow(2, Zoom)*TileSize))
		Lat = 1-Lat
		Lat = Lat * math.pi
		Lat = math.degrees(math.atan(math.sinh(Lat)))

		# print "LAT: {:f} LON: {:f}".format(Lat,Lon)
		return Lat,Lon

	# def LatLon2Px(self,z,lat,lon):
	# 	x = 2**z*(float(lon)+180)/360*256
	# 	y = -(.5*math.log((1+math.sin(math.radians(float(lat))))/(1-math.sin(math.radians(float(lat)))))/math.pi-1)*256*2**(z-1)
	# 	return x,y

	# def LatLon2XY(self,z,lat,lon):
	# 	x,y = self.LatLon2Px(z,lat,lon)
	# 	x = int(math.trunc(x/256))#,int(x%256)
	# 	y = int(math.trunc(y/256))#,int(y%256)
		return x,y

	def getLyrs(self, mt):
		if(mt == "roadsonly"):
			return 'h'
		elif(mt == "roadmap"):
			return 'm'
		elif(mt == "terrain"):
			return 'p'
		elif(mt == "roadmap2"):
			return 'r'
		elif(mt == "satellite"):
			return 's'
		elif(mt == "terrain"):
			return 't'
		elif(mt == "hybrid"):
			return 'y'
		else:
			return 's'


		# h = roads only
		# m = standard roadmap
		# p = terrain
		# r = somehow altered roadmap
		# s = satellite only
		# t = terrain only
		# y = hybrid






if __name__ == "__main__":
	rrmapimg = RRMapImage(800, 600, -23.8819352, -49.8170642, 10, "roadmap2")
    
#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter
from Tkinter import Tk, Canvas, Label, Frame, IntVar, Radiobutton, Button
from PIL import ImageTk
from ttk import *
from threading import Timer
import copy
import os

from RRMapImg import RRMapImage

LATITUDE  = -23.879908
LONGITUDE = -49.803486
ZOOM = 10
MAPTYPE = 'satellite'
KMLFILE = 'example.kml'

class UI(Tk):

	def __init__(self):

		Tk.__init__(self)

		#Default size
		self.width = 1000
		self.height = 600

		#Create window
		self.geometry('%dx%d+500+500' % (self.width,self.height))
		self.title('RRMaps')

		#Create canvas and label for map image
		self.canvas = Canvas(self, width=self.width, height=self.height)
		self.canvas.pack(fill='both', expand='YES')
		self.label = Label(self.canvas)

		#Events
		self.bind("<Key>", self.check_quit)
		self.bind('<B1-Motion>', self.drag)
		self.bind('<Button-1>', self.click)
		self.bind('<Configure>', self.resize)

		#Timer for resizing
		self.timer_resize = 0
		self.timer_resize_en = 0

		#Load list of maps
		self.LoadMapsList()

		#Default zoom
		self.zoomlevel = ZOOM

		#Draw toolbar
		self.draw_top_bar()

		#Create map
		self.RRMap = RRMapImage(self.width, self.height, LATITUDE, LONGITUDE, ZOOM, MAPTYPE)

		#Redraw
		self.restart()

	def LoadMapsList(self):
		self.maplist = []
		for file in os.listdir("maps/"):
			if file.endswith(".kml"):
				self.maplist.append(file)


	def draw_top_bar(self):
		#Frame
		# self.top_bar_frame = Frame(self.canvas)

		#Map selection
		self.map_selection_value = ''
		self.map_selection = Combobox(self.canvas, textvariable=self.map_selection_value, width="50", state='readonly')
		self.map_selection['values'] = self.maplist
		self.map_selection.current(0)
		self.map_selection.bind("<<ComboboxSelected>>", self.new_map_selection)

		#Marker selection
		self.marker_selection_value = ''
		self.marker_selection = Combobox(self.canvas, textvariable=self.marker_selection_value, width="15", state='readonly')
		self.marker_selection['values'] = ('X', 'Y', 'Z')
		self.marker_selection.current(0)
		self.marker_selection.bind("<<ComboboxSelected>>", self.new_marker_selection)

		#Map Type selection
		self.map_type_selection_value = ''
		self.map_type_selection = Combobox(self.canvas, textvariable=self.map_type_selection_value, width="10", state='readonly')
		self.map_type_selection['values'] = ('Satellite','Road Map','Terrain','Road Map 2','Roads Only','Terrain','Hybrid')
		self.map_type_selection.current(0)
		self.map_type_selection.bind("<<ComboboxSelected>>", self.new_map_type_selection)		

		#Zoom buttons
		self.zoom_in_button  = Tkinter.Button(self.canvas, text='+', borderwidth=1, command=lambda:self.zoom(+1))
		self.zoom_out_button = Tkinter.Button(self.canvas, text='-', borderwidth=1, command=lambda:self.zoom(-1))

	def place_top_bar(self):
		#Default variables
		line_y = 7
		cursor_x = self.width

		#Place components
		self.map_selection.place(x=50, y=line_y, width=cursor_x-510 )
		self.marker_selection.place(x=cursor_x-400, y=line_y)
		self.map_type_selection.place(x=cursor_x - 210, y=line_y )
		self.zoom_in_button.place(x= cursor_x - 30, y=line_y, height=18, width=20 )
		self.zoom_out_button.place(x= cursor_x - 50, y=line_y, height=18, width=20 )

	def new_map_type_selection(self,event):
		self.usemap(self.map_type_selection.current())
		self.map_type_selection.selection_clear()
		print "Type: ", self.map_type_selection.current()

	def new_map_selection(self, event):
		self.map_selection_value = self.map_selection.get()
		self.map_selection.selection_clear()
		print "Map: ", self.map_selection_value

		self.RRMap.SetMapKML('maps/'+self.map_selection_value)
		self.redraw()

	def new_marker_selection(self, event):
		self.marker_selection_value = self.marker_selection.get()
		self.marker_selection.selection_clear()
		print "Marker: ",self.marker_selection_value

	def reload(self):
		self.minsize(800,600)
		self.coords = None
		self.redraw()
		self['cursor']  = ''


	def restart(self):

		# A little trick to get a watch cursor along with loading
		self['cursor']  = 'watch'
		self.after(1, self.reload)

		

	def click(self, event):

		self.coords = event.x, event.y
		print "click",event.x,event.y

	def drag(self, event):

		self.RRMap.MoveXY(self.coords[0]-event.x, self.coords[1]-event.y)
		self.coords = event.x, event.y
		self.redraw()
		pass

	def resize(self, event):

		# print event.widget
		canvas = event.widget

		if (self.width != event.width or self.height != event.height) and canvas == self.canvas:
			if self.timer_resize_en == 1:
				# print "Reseting resize timer"
				self.timer_resize.cancel()
			self.timer_resize = Timer(0.25, self.resize_timeout)
			self.timer_resize.start()
			self.timer_resize_en = 1
				
			# print event.width, event.height
			self.width = event.width
			self.height = event.height

	def resize_timeout(self):
		# print "Resize timeout"
		self.timer_resize_en = 0
		self.redraw()


	def redraw(self):
		self.image = self.RRMap.GenerateImg(self.width,self.height)
		self.image_tk = ImageTk.PhotoImage(self.image)
		self.label['image'] = self.image_tk

		self.label.place(x=0, y=0, width=self.width, height=self.height) 

		

		self.place_top_bar()

	def usemap(self, maptypeidx):
		lyrs = ""
		if(maptypeidx == 0):
			lyrs = 's'
		elif(maptypeidx == 1):
			lyrs = 'm'
		elif(maptypeidx == 2):
			lyrs = 'p'
		elif(maptypeidx == 3):
			lyrs = 'r'
		elif(maptypeidx == 4):
			lyrs = 'h'
		elif(maptypeidx == 5):
			lyrs = 't'
		elif(maptypeidx == 6):
			lyrs = 'y'
		else:
			lyrs = 's'

		self.RRMap.SetMapLyrs(lyrs)
		self.RRMap.MoveXY(0, 0)
		self.redraw()
		pass

	def zoom(self, sign):

		newlevel = self.zoomlevel + sign
		if newlevel > 0 and newlevel < 22:
		 	self.zoomlevel = newlevel
		 	self.RRMap.SetZoom(newlevel)
		 	self.RRMap.MoveXY(self.width/2, self.height/2)
		 	self.redraw()
		pass

	def check_quit(self, event):
		if (event.char) != "":
			if ord(event.char) == 27: # ESC
				exit(0)

UI().mainloop()

#!/usr/bin/python
# -*- coding: utf-8 -*-
##
## Tile downloading
##

import os, sys, urllib2, time, random
from PIL import Image

class RRMapDownload():

    def __init__(self):
        pass
        # self.DownloadTile();
    
    def SetParams(self, TileX = 0, TileY = 0, Zoom = 10, Lyrs = 's'):

        self.TileX = TileX
        self.TileY = TileY
        self.Zoom = Zoom
        self.Lyrs = Lyrs

    def DownloadXYZ(self, TileX = 0, TileY = 0, Zoom = 10, Lyrs = 's'):

        folder = 'cache/'

        self.SetParams(TileX, TileY, Zoom, Lyrs)

        user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1'
        headers = { 'User-Agent' : user_agent }

        url = None
        filename = None
        #should work for mt0 to mt3
        url = "https://mt2.google.com/vt/lyrs=%s&?x=%d&s=&y=%d&z=%d" % (Lyrs, TileX, TileY, Zoom)
        print url

        if not(os.path.isdir(folder)):
            os.mkdir(folder, 0755 );

        filename = folder+"%d_%d_%d_%s.jpg" % (Zoom, TileX, TileY, Lyrs)

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

        return Image.open(filename)
        

            
#!/usr/bin/python

import urllib2
import os, sys
from gmap_utils import *

import time
import random

def download_tiles(zoom, lat_start, lat_stop, lon_start, lon_stop, satellite=True, folder='tmp/'):

    start_x, start_y = latlon2xy(zoom, lat_start, lon_start)
    stop_x, stop_y = latlon2xy(zoom, lat_stop, lon_stop)

    if(start_x>stop_x):
        start_x1 = start_x; start_x = stop_x; stop_x = start_x1;
    if(start_y>stop_y):
        start_y1 = start_y; start_y = stop_y; stop_y = start_y1;
    
    print "x range", start_x, stop_x
    print "y range", start_y, stop_y
    
    user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1'
    headers = { 'User-Agent' : user_agent }
    
    for x in xrange(start_x, stop_x):
        for y in xrange(start_y, stop_y):
            
            url = None
            filename = None
            
            # h = roads only
            # m = standard roadmap
            # p = terrain
            # r = somehow altered roadmap
            # s = satellite only
            # t = terrain only
            # y = hybrid
            if satellite:    
                lyrs = 's'    
                
            else:
                lyrs = 'm'
            
            url = "https://mt0.google.com/vt/lyrs=%s&?x=%d&s=&y=%d&z=%d" % (lyrs, x, y, zoom)

            if not(os.path.isdir(folder)):
                os.mkdir(folder, 0755 );

            filename = folder+"%d_%d_%d_%s.jpg" % (zoom, x, y, lyrs)
    
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

if __name__ == "__main__":
    
    zoom = 15

    lat_start, lon_start = 46.53, 6.6
    lat_stop, lon_stop = 46.49, 6.7
        
    download_tiles(zoom, lat_start, lat_stop, lon_start, lon_stop, satellite=True, folder=temp_folder)

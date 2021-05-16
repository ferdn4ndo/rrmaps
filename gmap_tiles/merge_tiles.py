from PIL import Image
import sys, os
from gmap_utils import *

def merge_tiles(zoom, lat_start, lat_stop, lon_start, lon_stop, satellite=True, folder='tmp/'):
    
    TYPE, ext = 'r', 'png'
    if satellite:
        TYPE, ext = 's', 'jpg'
    
    x_start, y_start = latlon2xy(zoom, lat_start, lon_start)
    x_stop, y_stop = latlon2xy(zoom, lat_stop, lon_stop)

    if(x_start>x_stop):
        x_start1 = x_start; x_start = x_stop; x_stop = x_start1;
    if(y_start>y_stop):
        y_start1 = y_start; y_start = y_stop; y_stop = y_start1;
    
    print "x range", x_start, x_stop
    print "y range", y_start, y_stop
    
    w = (x_stop - x_start) * 256
    h = (y_stop - y_start) * 256
    
    print "width:", w
    print "height:", h
    
    result = Image.new("RGBA", (w, h))
    
    for x in xrange(x_start, x_stop):
        for y in xrange(y_start, y_stop):
            
            filename = "%d_%d_%d_%s.%s" % (zoom, x, y, TYPE, ext)
            
            if not os.path.exists(folder+filename):
                print "-- missing", filename
                continue
                    
            x_paste = (x - x_start) * 256
            y_paste = h - (y_stop - y) * 256
            
            try:
                i = Image.open(folder+filename)
            except Exception, e:
                print "-- %s, removing %s" % (e, folder+filename)
                trash_dst = os.path.expanduser("~/.Trash/%s" % folder+filename)
                os.rename(folder+filename, trash_dst)
                continue
            
            result.paste(i, (x_paste, y_paste))
            
            del i
    
    result.save("map_%s.%s" % (TYPE, ext))

if __name__ == "__main__":
    
    zoom = 15

    lat_start, lon_start = 46.53, 6.6
    lat_stop, lon_stop = 46.49, 6.7
    
    merge_tiles(zoom, lat_start, lat_stop, lon_start, lon_stop, satellite=True, folder='tmp/')

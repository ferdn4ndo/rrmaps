# http://oregonarc.com/2011/02/command-line-tile-cutter-for-google-maps-improved/
# http://media.oregonarc.com/fish/tile.py

import math

def latlon2px(z,lat,lon):
    x = 2**z*(float(lon)+180)/360*256
    y = -(.5*math.log((1+math.sin(math.radians(float(lat))))/(1-math.sin(math.radians(float(lat)))))/math.pi-1)*256*2**(z-1)
    return x,y

def latlon2xy(z,lat,lon):
    x,y = latlon2px(z,lat,lon)
    x = int(math.trunc(x/256))#,int(x%256)
    y = int(math.trunc(y/256))#,int(y%256)
    return x,y

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
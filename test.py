import os
from PIL import Image
import rasterio
import rasterio.features
import rasterio.warp
from osgeo import gdal
from xml.dom import minidom
import xml.etree.ElementTree
yourpath = os.getcwd()
width=830
height=700
for root, dirs, files in os.walk(yourpath, topdown=False):
    for name in files:
        print(os.path.join(root, name))
        completePath=os.path.join(root, name)
        splitName=os.path.splitext(completePath)
        #print(splitName[len(splitName)-1].lower())
        if splitName[len(splitName)-1].lower() == ".xml":
            if os.path.isfile(os.path.splitext(os.path.join(root, name))[0] + ".png"):
                print("A jpeg file already exists for %s" % name)
            # If a jpeg is *NOT* present, create one from the tiff.
            else:
                e = xml.etree.ElementTree.parse(completePath).getroot()
                #print(e)
                padfTransform=[]
                for atype in e.findall('GeoTransform'):
                    padfTransform = atype.text.split(',')
                #print(padfTransform[0])
                xp = padfTransform[0] + width*padfTransform[1] + height*padfTransform[2]   
                yp = float(padfTransform[3]) + width*float(padfTransform[4]) + height*float(padfTransform[5])
                #print(xp)
                print(yp)

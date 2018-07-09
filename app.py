import os
from PIL import Image
import rasterio
import rasterio.features
import rasterio.warp
from osgeo import osr, gdal
yourpath = os.getcwd()
for root, dirs, files in os.walk(yourpath, topdown=False):
    for name in files:
        #print(os.path.join(root, name))
        completePath=os.path.join(root, name)
        splitName=os.path.splitext(completePath)
        #print(splitName[len(splitName)-1].lower())
        if splitName[len(splitName)-1].lower() == ".png":
            if os.path.isfile(os.path.splitext(os.path.join(root, name))[0] + ".tif"):
                print("A jpeg file already exists for %s" % name)
            # If a jpeg is *NOT* present, create one from the tiff.
            else:
                ds = gdal.Open(completePath)
                old_cs= osr.SpatialReference()
                old_cs.ImportFromWkt(ds.GetProjectionRef())
                width = ds.RasterXSize
                height = ds.RasterYSize
                gt = ds.GetGeoTransform()
                wgs84_wkt = """
                GEOGCS["WGS 84",
                    DATUM["WGS_1984",
                        SPHEROID["WGS 84",6378137,298.257223563,
                            AUTHORITY["EPSG","7030"]],
                        AUTHORITY["EPSG","6326"]],
                    PRIMEM["Greenwich",0,
                        AUTHORITY["EPSG","8901"]],
                    UNIT["degree",0.01745329251994328,
                        AUTHORITY["EPSG","9122"]],
                    AUTHORITY["EPSG","4326"]]"""
                new_cs = osr.SpatialReference()
                new_cs .ImportFromWkt(wgs84_wkt)

                # create a transform object to convert between coordinate systems
                transform = osr.CoordinateTransformation(old_cs,new_cs)
                minx = gt[0]
                miny = gt[3] + width*gt[4] + height*gt[5] 
                maxx = gt[0] + width*gt[1] + height*gt[2]
                maxy = gt[3]
                #latlongmin=tranform.TransformPoint(minx,miny)
                print(transform.TransformPoint(minx,miny))
                print(transform.TransformPoint(maxx,maxy))

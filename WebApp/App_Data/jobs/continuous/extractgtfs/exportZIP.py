import itertools
import os
import StringIO
import zipfile

import shapefile

def process(schedule, parsedpath):

    prj = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]'

    print("shapes.zip")
    #export shapes
    shp = StringIO.StringIO()
    shx = StringIO.StringIO()
    dbf = StringIO.StringIO()
    writer = shapefile.Writer(shapefile.POLYLINE)
    writer.field("shape_id", "C", "6")
    writer.field("direction", "C", "1")
    writer.field("headsign", "C", "64")
    writer.field("short_name", "C", "4")
    writer.field("long_name", "C", "64")
    writer.field("color", "C", "6")
    tripList = schedule.GetTripList()
    sortedTrips = sorted(tripList, key=lambda item: item.shape_id)
    for shape_id, trips in itertools.groupby(sortedTrips, key=lambda item: item.shape_id):
        trip = next(trips)
        route = schedule.GetRoute(trip.route_id)
        shape = schedule.GetShape(shape_id)
        writer.line(parts=[[[point[1], point[0]] for point in shape.points]])
        writer.record(shape.shape_id, trip.direction_id, trip.trip_headsign.replace(u'\u21b6',"").replace(u'\u21b7' ,""), route.route_short_name, route.route_long_name, route.route_color)
    writer.saveShp(shp)
    writer.saveShx(shx)
    writer.saveDbf(dbf)
    zipFile = zipfile.ZipFile(os.path.join(parsedpath, "shapes.zip"), "w", zipfile.ZIP_DEFLATED)
    zipFile.writestr("shapes.shp", shp.getvalue())
    zipFile.writestr("shapes.shx", shx.getvalue())
    zipFile.writestr("shapes.dbf", dbf.getvalue())
    zipFile.writestr("shapes.prj", prj)
    zipFile.close()

    print("stops.zip")
    #export stops
    shp = StringIO.StringIO()
    shx = StringIO.StringIO()
    dbf = StringIO.StringIO()
    writer = shapefile.Writer(shapefile.POINT)
    writer.field("stop_id", "C", "4")
    writer.field("stop_code", "C", "4")
    writer.field("stop_name", "C", "64")
    writer.field("stop_desc", "C", "64")
    stopList = schedule.GetStopList()
    for stop in stopList:
        writer.point(stop.stop_lon, stop.stop_lat)
        writer.record(stop.stop_id, stop.stop_code, stop.stop_name, stop.stop_desc)
    writer.saveShp(shp)
    writer.saveShx(shx)
    writer.saveDbf(dbf)
    zipFile = zipfile.ZipFile(os.path.join(parsedpath, "stops.zip"), "w", zipfile.ZIP_DEFLATED)
    zipFile.writestr("stops.shp", shp.getvalue())
    zipFile.writestr("stops.shx", shx.getvalue())
    zipFile.writestr("stops.dbf", dbf.getvalue())
    zipFile.writestr("stops.prj", prj)
    zipFile.close()

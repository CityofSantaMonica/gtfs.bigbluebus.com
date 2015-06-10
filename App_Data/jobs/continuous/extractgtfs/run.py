import itertools
import json
import operator
import os
import sys
from time import sleep
import zipfile

import transitfeed

currentzippath = "/home/site/wwwroot/current.zip"
previous_mtime = 0

while True:
    currentzipstat = os.stat(currentzippath)
    if previous_mtime != currentzipstat.st_mtime:
        print "GTFS:" + str(currentzipstat.st_mtime)

        if zipfile.is_zipfile(currentzippath):
            currentzip = zipfile.ZipFile(currentzippath,'r')
            currentzip.extractall("/home/site/wwwroot/csv")

            schedule = transitfeed.Schedule()
            trip = transitfeed.Trip()
            route = transitfeed.Route()
            #shape = transitfeed.Shape()

            #export trips for live map
            schedule.Load(currentzippath)
            tripList = schedule.GetTripList()
            forJson = {}
            for trip in tripList:
                route = schedule.GetRoute(trip.route_id)
                x = {"trip_id" : trip.trip_id, "direction_id" : trip.direction_id, "route_id" : trip.route_id, "route_short_name" : route.route_short_name, "route_long_name" : route.route_long_name, "route_color" : route.route_color}
                forJson[trip.trip_id] = x
            json.dump(forJson, open("/home/site/wwwroot/gtfs/trips.json","w"))

            #export shapes with route information
            shapeList = schedule.GetShapeList()
            features = []
            sortedTrips = sorted(tripList, key=lambda item: item.shape_id)
            for shape_id, trips in itertools.groupby(sortedTrips, key=lambda item: item.shape_id):
                trip = next(trips)
                route = schedule.GetRoute(trip.route_id)
                shape = schedule.GetShape(shape_id)
                feature = {"type": "Feature", "properties": { "shape_id": shape.shape_id, "direction_id":trip.direction_id, "route_short_name" : route.route_short_name, "route_long_name" : route.route_long_name, "route_color" : route.route_color }, "geometry" : { "type": "LineString","coordinates": [[point[1], point[0]] for point in shape.points] } }
                features.append(feature)
            forJson = {"type": "FeatureCollection","crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } }, "features": features }
            json.dump(forJson, open("/home/site/wwwroot/gis/shapes.geojson","w"))

        previous_mtime = currentzipstat.st_mtime
    else:
        sleep(60)
    
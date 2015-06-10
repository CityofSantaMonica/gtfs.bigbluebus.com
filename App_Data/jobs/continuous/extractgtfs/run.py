import json
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

            schedule.Load(currentzippath)
            tripList = schedule.GetTripList()
            forJson = {}
            for trip in tripList:
                route = schedule.GetRoute(trip.route_id)
                x = {"trip_id" : trip.trip_id, "direction_id" : trip.direction_id, "route_id" : trip.route_id, "route_short_name" : route.route_short_name, "route_long_name" : route.route_long_name, "route_color" : route.route_color}
                forJson[trip.trip_id] = x
            json.dump(forJson, open("/home/site/wwwroot/gtfs/trips.json","w"))
        previous_mtime = currentzipstat.st_mtime
    else:
        sleep(60)
    
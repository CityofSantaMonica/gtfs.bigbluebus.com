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

            #export trips for live map
            schedule.Load(currentzippath)
            tripList = schedule.GetTripList()
            forJson = {}
            for trip in tripList:
                route = schedule.GetRoute(trip.route_id)
                x = {"trip_id" : trip.trip_id, "direction_id" : trip.direction_id, "route_id" : trip.route_id, "route_short_name" : route.route_short_name, "route_long_name" : route.route_long_name, "route_color" : route.route_color}
                forJson[trip.trip_id] = x
            json.dump(forJson, open("/home/site/wwwroot/gtfs/trips.json","w"))

            #export gtfs to json
            #agency.txt
            forJson = {}
            for agency in schedule.GetAgencyList():
                forJson[agency.agency_id] = {"agency_id" : agency.agency_id, "agency_name" : agency.agency_name, "agency_url" : agency.agency_url, "agency_timezone" : agency.agency_timezone, "agency_lang" : agency.agency_lang, "agency_phone" : agency.agency_phone, "agency_fare_url" : agency.agency_fare_url }
            json.dump(forJson, open("/home/site/wwwroot/json/agency.json","w"))

            #stops.txt
            forJson = {}
            for stop in schedule.GetStopList():
                forJson[stop.stop_id] = {"stop_id" : stop.stop_id, "stop_code" : stop.stop_code, "stop_name" : stop.stop_name, "stop_desc" : stop.stop_desc, "stop_lat" : stop.stop_lat, "stop_lon" : stop.stop_lon, "zone_id" : stop.zone_id, "stop_url" : stop.stop_url, "location_type" : stop.location_type, "parent_station" : stop.parent_station, "stop_timezone" : stop.stop_timezone, "wheelchair_boarding" : stop.wheelchair_boarding }
            json.dump(forJson, open("/home/site/wwwroot/json/stops.json","w"))

            #routes.txt
            forJson = {}
            for route in schedule.GetRouteList():
                forJson[route.route_id] = {"route_id" : route.route_id, "agency_id" : route.agency_id, "route_short_name" : route.route_short_name, "route_long_name" : route.route_long_name, "route_desc" : route.route_desc, "route_type" : route.route_type, "route_url" : route.route_url, "route_color" : route.route_color, "route_text_color" : route.route_text_color }
            json.dump(forJson, open("/home/site/wwwroot/json/routes.json","w"))

            #trips.txt
            forJson = {}
            for trip in schedule.GetTripList():
                forJson[trip.trip_id] = {"route_id" : trip.route_id, "service_id" : trip.service_id, "trip_id" : trip.trip_id, "trip_headsign" : trip.trip_headsign, "trip_short_name" : trip.trip_short_name, "direction_id" : trip.direction_id, "block_id" : trip.block_id, "shape_id" : trip.shape_id, "wheelchair_accessible" : trip.wheelchair_accessible, "bikes_allowed" : trip.bikes_allowed }
            json.dump(forJson, open("/home/site/wwwroot/json/trips.json","w"))

            #trips.txt
            forJson = {}
            for trip in schedule.GetTripList():
                stop_times = {}
                for stop_time in sorted(trip.GetStopTimes(), key=lambda item: item.stop_sequence):
                    stop_times[stop_time.stop_sequence] = {"trip_id" : trip.trip_id, "arrival_time" : stop_time.arrival_time, "departure_time" : stop_time.departure_time, "stop_id" : stop_time.stop_id, "stop_sequence" : stop_time.stop_sequence, "stop_headsign" : stop_time.stop_headsign, "pickup_type" : stop_time.pickup_type, "drop_off_type" : stop_time.drop_off_type, "shape_dist_traveled" : stop_time.shape_dist_traveled, "timepoint" : stop_time.timepoint }
                    forJson[trip.trip_id] = stop_times
            json.dump(forJson, open("/home/site/wwwroot/json/stop_times.json","w"))

            #calendar.txt
            forJson = {}
            for calendar in schedule.GetServicePeriodList():
                forJson[calendar.service_id] = {"service_id" : calendar.service_id, "monday" : calendar.monday, "tuesday" : calendar.tuesday, "wednesday" : calendar.wednesday, "thursday" : calendar.thursday, "friday" : calendar.friday, "saturday" : calendar.saturday, "sunday" : calendar.sunday, "start_date" : calendar.start_date, "end_date" : calendar.end_date }
            json.dump(forJson, open("/home/site/wwwroot/json/calendar.json","w"))

            #calendar_dates.txt
            forJson = []
            calendar = transitfeed.ServicePeriod()
            for calendar in schedule.GetServicePeriodList():
                for calendar_date in calendar.GetCalendarDatesFieldValuesTuples():
                    forJson.append({"service_id" : calendar_date[0], "date" : calendar_date[1], "exception_type" : calendar_date[2] })
            json.dump(forJson, open("/home/site/wwwroot/json/calendar_dates.json","w"))

            #fare_attributes.txt
            forJson = {}
            for fare_attribute in schedule.GetFareAttributeList():
                forJson[fare_attribute.fare_id] = {"fare_id" : fare_attribute.fare_id, "price" : fare_attribute.price, "currency_type" : fare_attribute.currency_type, "payment_method" : fare_attribute.payment_method, "transfers" : fare_attribute.transfers, "transfer_duration" : fare_attribute.transfer_duration }
            json.dump(forJson, open("/home/site/wwwroot/json/fare_attributes.json","w"))

            #fare_rules.txt
            forJson = []
            for fare_attribute in schedule.GetFareAttributeList():
                for fare_rule in fare_attribute.GetFareRuleList():
                    forJson.append({"fare_id" : fare_attribute.fare_id, "route_id" : fare_rule.route_id, "origin_id" : fare_rule.origin_id, "destination_id" : fare_rule.destination_id, "contains_id" : fare_rule.contains_id })
            json.dump(forJson, open("/home/site/wwwroot/json/fare_rules.json","w"))

            #shapes.txt
            forJson = {}
            for shape in schedule.GetShapeList():
                forJson[shape.shape_id] = { "shape_id" : shape.shape_id, "points" : [ { "shape_pt_lat" : point[0], "shape_pt_lon" : point[1]} for point in shape.points  ] }
            json.dump(forJson, open("/home/site/wwwroot/json/shapes.json","w"))
            
            #feed_info.txt

            #export shapes with route information
            shapeList = schedule.GetShapeList()
            features = []
            sortedTrips = sorted(tripList, key=lambda item: item.shape_id)
            for shape_id, trips in itertools.groupby(sortedTrips, key=lambda item: item.shape_id):
                trip = next(trips)
                route = schedule.GetRoute(trip.route_id)
                shape = schedule.GetShape(shape_id)
                feature = {"type": "Feature", "properties": { "shape_id" : shape.shape_id, "direction_id" : trip.direction_id, "route_short_name" : route.route_short_name, "route_long_name" : route.route_long_name, "route_color" : route.route_color }, "geometry" : { "type": "LineString","coordinates": [[point[1], point[0]] for point in shape.points] } }
                features.append(feature)
            forJson = {"type": "FeatureCollection","crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } }, "features": features }
            json.dump(forJson, open("/home/site/wwwroot/gis/shapes.geojson","w"))

            #export stops
            stopList = schedule.GetStopList()
            features = []
            for stop in stopList:
                feature =  {"type": "Feature", "properties": { "stop_id" : stop.stop_id, "stop_code": stop.stop_code, "stop_name" : stop.stop_name, "stop_desc" : stop.stop_desc}, "geometry" : { "type" : "Point", "coordinates" : [stop.stop_lon, stop.stop_lat] } }
                features.append(feature)
            forJson = {"type": "FeatureCollection","crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } }, "features": features }
            json.dump(forJson, open("/home/site/wwwroot/gis/stops.geojson","w"))

        previous_mtime = currentzipstat.st_mtime
    else:
        sleep(60)
    
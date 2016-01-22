import itertools
import json
import operator
import os
import StringIO
import sys
from time import sleep
import xml.etree.cElementTree as ET
import zipfile

import shapefile
import transitfeed

parsedpath = "/home/site/wwwroot/parsed"
currentzippath = "/home/site/wwwroot/current.zip"
previous_mtime = 0

if not os.path.exists(parsedpath):
    os.makedirs(parsedpath)

while True:
    currentzipstat = os.stat(currentzippath)
    if previous_mtime != currentzipstat.st_mtime:
        #print "GTFS:" + str(currentzipstat.st_mtime)

        if zipfile.is_zipfile(currentzippath):

            # export gtfs as csv

            currentzip = zipfile.ZipFile(currentzippath,'r')
            currentzip.extractall(parsedpath)

            #load gtfs from zip file

            schedule = transitfeed.Schedule()
            schedule.Load(currentzippath)



            #export gtfs as json

            #agency.txt
            forJson = {}
            for agency in schedule.GetAgencyList():
                forJson[agency.agency_id] = {"agency_id" : agency.agency_id, "agency_name" : agency.agency_name, "agency_url" : agency.agency_url, "agency_timezone" : agency.agency_timezone, "agency_lang" : agency.agency_lang, "agency_phone" : agency.agency_phone, "agency_fare_url" : agency.agency_fare_url }
            json.dump(forJson, open(os.path.join(parsedpath, "agency.json"),"w"))

            #stops.txt
            forJson = {}
            for stop in schedule.GetStopList():
                forJson[stop.stop_id] = {"stop_id" : stop.stop_id, "stop_code" : stop.stop_code, "stop_name" : stop.stop_name, "stop_desc" : stop.stop_desc, "stop_lat" : stop.stop_lat, "stop_lon" : stop.stop_lon, "zone_id" : stop.zone_id, "stop_url" : stop.stop_url, "location_type" : stop.location_type, "parent_station" : stop.parent_station, "stop_timezone" : stop.stop_timezone, "wheelchair_boarding" : stop.wheelchair_boarding }
            json.dump(forJson, open(os.path.join(parsedpath, "stops.json"),"w"))

            #routes.txt
            forJson = {}
            for route in schedule.GetRouteList():
                forJson[route.route_id] = {"route_id" : route.route_id, "agency_id" : route.agency_id, "route_short_name" : route.route_short_name, "route_long_name" : route.route_long_name, "route_desc" : route.route_desc, "route_type" : route.route_type, "route_url" : route.route_url, "route_color" : route.route_color, "route_text_color" : route.route_text_color }
            json.dump(forJson, open(os.path.join(parsedpath, "routes.json"),"w"))

            #trips.txt
            forJson = {}
            for trip in schedule.GetTripList():
                forJson[trip.trip_id] = {"route_id" : trip.route_id, "service_id" : trip.service_id, "trip_id" : trip.trip_id, "trip_headsign" : trip.trip_headsign, "trip_short_name" : trip.trip_short_name, "direction_id" : trip.direction_id, "block_id" : trip.block_id, "shape_id" : trip.shape_id, "wheelchair_accessible" : trip.wheelchair_accessible, "bikes_allowed" : trip.bikes_allowed }
            json.dump(forJson, open(os.path.join(parsedpath, "trips.json"),"w"))

            #stop_times.txt
            forJson = {}
            for trip in schedule.GetTripList():
                stop_times = {}
                for stop_time in sorted(trip.GetStopTimes(), key=lambda item: item.stop_sequence):
                    stop_times[stop_time.stop_sequence] = {"trip_id" : trip.trip_id, "arrival_time" : stop_time.arrival_time, "departure_time" : stop_time.departure_time, "stop_id" : stop_time.stop_id, "stop_sequence" : stop_time.stop_sequence, "stop_headsign" : stop_time.stop_headsign, "pickup_type" : stop_time.pickup_type, "drop_off_type" : stop_time.drop_off_type, "shape_dist_traveled" : stop_time.shape_dist_traveled, "timepoint" : stop_time.timepoint }
                    forJson[trip.trip_id] = stop_times
            json.dump(forJson, open(os.path.join(parsedpath, "stop_times.json"),"w"))

            #calendar.txt
            forJson = {}
            for calendar in schedule.GetServicePeriodList():
                forJson[calendar.service_id] = {"service_id" : calendar.service_id, "monday" : calendar.monday, "tuesday" : calendar.tuesday, "wednesday" : calendar.wednesday, "thursday" : calendar.thursday, "friday" : calendar.friday, "saturday" : calendar.saturday, "sunday" : calendar.sunday, "start_date" : calendar.start_date, "end_date" : calendar.end_date }
            json.dump(forJson, open(os.path.join(parsedpath, "calendar.json"),"w"))

            #calendar_dates.txt
            forJson = []
            calendar = transitfeed.ServicePeriod()
            for calendar in schedule.GetServicePeriodList():
                for calendar_date in calendar.GetCalendarDatesFieldValuesTuples():
                    forJson.append({"service_id" : calendar_date[0], "date" : calendar_date[1], "exception_type" : calendar_date[2] })
            json.dump(forJson, open(os.path.join(parsedpath, "calendar_dates.json"),"w"))

            #fare_attributes.txt
            forJson = {}
            for fare_attribute in schedule.GetFareAttributeList():
                forJson[fare_attribute.fare_id] = {"fare_id" : fare_attribute.fare_id, "price" : fare_attribute.price, "currency_type" : fare_attribute.currency_type, "payment_method" : fare_attribute.payment_method, "transfers" : fare_attribute.transfers, "transfer_duration" : fare_attribute.transfer_duration }
            json.dump(forJson, open(os.path.join(parsedpath, "fare_attributes.json"),"w"))

            #fare_rules.txt
            forJson = []
            for fare_attribute in schedule.GetFareAttributeList():
                for fare_rule in fare_attribute.GetFareRuleList():
                    forJson.append({"fare_id" : fare_attribute.fare_id, "route_id" : fare_rule.route_id, "origin_id" : fare_rule.origin_id, "destination_id" : fare_rule.destination_id, "contains_id" : fare_rule.contains_id })
            json.dump(forJson, open(os.path.join(parsedpath, "fare_rules.json"),"w"))

            #shapes.txt
            forJson = {}
            for shape in schedule.GetShapeList():
                forJson[shape.shape_id] = { "shape_id" : shape.shape_id, "points" : [ { "shape_pt_lat" : point[0], "shape_pt_lon" : point[1]} for point in shape.points  ] }
            json.dump(forJson, open(os.path.join(parsedpath, "shapes.json"),"w"))
            


            #export gtfs as xml
            ET.register_namespace("","http://gtfs.bigbluebus.com/gtfs.xsd")
            ET.register_namespace("xsi","http://www.w3.org/2001/XMLSchema-instance")

            #agency.txt
            root = ET.Element("{http://gtfs.bigbluebus.com/gtfs.xsd}gtfs", { "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation" : "http://gtfs.bigbluebus.com/ gtfs.xsd" })
            agencies = ET.SubElement(root, "{http://gtfs.bigbluebus.com/gtfs.xsd}agencies")
            for agency in schedule.GetAgencyList():
                item = ET.SubElement(agencies, "{http://gtfs.bigbluebus.com/gtfs.xsd}agency", { "agency_name" : agency.agency_name, "agency_url" : agency.agency_url, "agency_timezone" : agency.agency_timezone })
                if agency.agency_id:
                    item.set("agency_id", agency.agency_id)
                if agency.agency_lang:
                    item.set("agency_lang", agency.agency_lang)
                if agency.agency_phone:
                    item.set("agency_phone", agency.agency_phone)
                if agency.agency_fare_url:
                    item.set("agency_fare_url", agency.agency_fare_url)
            tree = ET.ElementTree(root)
            tree.write(os.path.join(parsedpath, "agency.xml"), xml_declaration=True, encoding='utf-8', method="xml")

            #stops.txt
            root = ET.Element("{http://gtfs.bigbluebus.com/gtfs.xsd}gtfs", { "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation" : "http://gtfs.bigbluebus.com/ gtfs.xsd" })
            stops = ET.SubElement(root, "{http://gtfs.bigbluebus.com/gtfs.xsd}stops")
            for stop in schedule.GetStopList():
                item = ET.SubElement(stops, "{http://gtfs.bigbluebus.com/gtfs.xsd}stop", {"stop_id" : stop.stop_id, "stop_name" : stop.stop_name, "stop_lat" : str(stop.stop_lat), "stop_lon" : str(stop.stop_lon) })
                if stop.stop_code:
                    item.set("stop_code", stop.stop_code)
                if stop.stop_desc:
                    item.set("stop_desc", stop.stop_desc)
                if stop.zone_id:
                    item.set("zone_id", stop.zone_id)
                if stop.stop_url:
                    item.set("stop_url", stop.stop_url)
                if stop.location_type:
                    item.set("location_type", stop.location_type)
                if stop.parent_station:
                    item.set("parent_station", stop.parent_station)
                if stop.stop_timezone:
                    item.set("stop_timezone", stop.stop_timezone)
                if stop.wheelchair_boarding:
                    item.set("wheelchair_boarding", stop.wheelchair_boarding)
            tree = ET.ElementTree(root)
            tree.write(os.path.join(parsedpath, "stops.xml"), xml_declaration=True, encoding='utf-8', method="xml")

            #routes.txt
            root = ET.Element("{http://gtfs.bigbluebus.com/gtfs.xsd}gtfs", { "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation" : "http://gtfs.bigbluebus.com/ gtfs.xsd" })
            routes = ET.SubElement(root, "{http://gtfs.bigbluebus.com/gtfs.xsd}routes")
            for route in schedule.GetRouteList():
                item = ET.SubElement(routes, "{http://gtfs.bigbluebus.com/gtfs.xsd}route", {"route_id" : route.route_id, "route_short_name" : route.route_short_name, "route_long_name" : route.route_long_name, "route_type" : str(route.route_type) })
                if route.agency_id:
                    item.set("agency_id", route.agency_id)
                if route.route_desc:
                    item.set("route_desc", route.route_desc)
                if route.route_url:
                    item.set("route_url", route.route_url)
                if route.route_color:
                    item.set("route_color", route.route_color)
                if route.route_text_color:
                    item.set("route_text_color", route.route_text_color)
            tree = ET.ElementTree(root)
            tree.write(os.path.join(parsedpath, "routes.xml"), xml_declaration=True, encoding='utf-8', method="xml")

            #trips.txt
            root = ET.Element("{http://gtfs.bigbluebus.com/gtfs.xsd}gtfs", { "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation" : "http://gtfs.bigbluebus.com/ gtfs.xsd" })
            trips = ET.SubElement(root, "{http://gtfs.bigbluebus.com/gtfs.xsd}trips")
            for trip in schedule.GetTripList():
                item = ET.SubElement(trips, "{http://gtfs.bigbluebus.com/gtfs.xsd}trip", {"route_id" : trip.route_id, "service_id" : trip.service_id, "trip_id" : trip.trip_id })
                if trip.trip_headsign:
                    item.set("trip_headsign", trip.trip_headsign)
                if trip.trip_short_name:
                    item.set("trip_short_name", trip.trip_short_name)
                if trip.direction_id:
                    item.set("direction_id", trip.direction_id)
                if trip.block_id:
                    item.set("block_id", trip.block_id)
                if trip.shape_id:
                    item.set("shape_id", trip.shape_id)
                if trip.wheelchair_accessible:
                    item.set("wheelchair_accessible", trip.wheelchair_accessible)
                if trip.bikes_allowed:
                    item.set("bikes_allowed", trip.bikes_allowed)
            tree = ET.ElementTree(root)
            tree.write(os.path.join(parsedpath, "trips.xml"), xml_declaration=True, encoding='utf-8', method="xml")

            #stop_times.txt
            root = ET.Element("{http://gtfs.bigbluebus.com/gtfs.xsd}gtfs", { "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation" : "http://gtfs.bigbluebus.com/ gtfs.xsd" })
            stop_times = ET.SubElement(root, "{http://gtfs.bigbluebus.com/gtfs.xsd}stop_times")
            for trip in schedule.GetTripList():
                for stop_time in sorted(trip.GetStopTimes(), key=lambda item: item.stop_sequence):
                    item = ET.SubElement(stop_times, "{http://gtfs.bigbluebus.com/gtfs.xsd}stop_time", {"trip_id" : trip.trip_id, "arrival_time" : stop_time.arrival_time, "departure_time" : stop_time.departure_time, "stop_id" : stop_time.stop_id, "stop_sequence" : str(stop_time.stop_sequence) })
                    if stop_time.stop_headsign:
                        item.set("stop_headsign", stop_time.stop_headsign)
                    if stop_time.pickup_type:
                        item.set("pickup_type", str(stop_time.pickup_type))
                    if stop_time.drop_off_type:
                        item.set("drop_off_type", str(stop_time.drop_off_type))
                    if stop_time.shape_dist_traveled:
                        item.set("shape_dist_traveled", str(stop_time.shape_dist_traveled))
                    if stop_time.timepoint:
                        item.set("timepoint", str(stop_time.timepoint))
            tree = ET.ElementTree(root)
            tree.write(os.path.join(parsedpath, "stop_times.xml"), xml_declaration=True, encoding='utf-8', method="xml")

            #calendar.txt
            root = ET.Element("{http://gtfs.bigbluebus.com/gtfs.xsd}gtfs", { "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation" : "http://gtfs.bigbluebus.com/ gtfs.xsd" })
            calendar = ET.SubElement(root, "{http://gtfs.bigbluebus.com/gtfs.xsd}calendar")
            for servicePeriod in schedule.GetServicePeriodList():
                item = ET.SubElement(calendar, "{http://gtfs.bigbluebus.com/gtfs.xsd}service", {"service_id" : servicePeriod.service_id, "monday" : str(servicePeriod.monday), "tuesday" : str(servicePeriod.tuesday), "wednesday" : str(servicePeriod.wednesday), "thursday" : str(servicePeriod.thursday), "friday" : str(servicePeriod.friday), "saturday" : str(servicePeriod.saturday), "sunday" : str(servicePeriod.sunday), "start_date" : servicePeriod.start_date, "end_date" : servicePeriod.end_date })
            tree = ET.ElementTree(root)
            tree.write(os.path.join(parsedpath, "calendar.xml"), xml_declaration=True, encoding='utf-8', method="xml")

            #calendar_dates.txt
            root = ET.Element("{http://gtfs.bigbluebus.com/gtfs.xsd}gtfs", { "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation" : "http://gtfs.bigbluebus.com/ gtfs.xsd" })
            calendar_dates = ET.SubElement(root, "{http://gtfs.bigbluebus.com/gtfs.xsd}calendar_dates")
            calendar = transitfeed.ServicePeriod()
            for calendar in schedule.GetServicePeriodList():
                for calendar_date in calendar.GetCalendarDatesFieldValuesTuples():
                    item = ET.SubElement(calendar_dates, "{http://gtfs.bigbluebus.com/gtfs.xsd}calendar_date", { "service_id" : calendar_date[0], "date" : calendar_date[1], "exception_type" : calendar_date[2] })
            tree = ET.ElementTree(root)
            tree.write(os.path.join(parsedpath, "calendar_dates.xml"), xml_declaration=True, encoding='utf-8', method="xml")

            #fare_attributes.txt
            root = ET.Element("{http://gtfs.bigbluebus.com/gtfs.xsd}gtfs", { "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation" : "http://gtfs.bigbluebus.com/ gtfs.xsd" })
            fare_attributes = ET.SubElement(root, "{http://gtfs.bigbluebus.com/gtfs.xsd}fare_attributes")
            for fare_attribute in schedule.GetFareAttributeList():
                item = ET.SubElement(fare_attributes, "{http://gtfs.bigbluebus.com/gtfs.xsd}fare_attribute", {"fare_id" : fare_attribute.fare_id, "price" : str(fare_attribute.price), "currency_type" : str(fare_attribute.currency_type), "payment_method" : str(fare_attribute.payment_method), "transfers" : str(fare_attribute.transfers) })
                if fare_attribute.transfer_duration:
                    item.set("transfer_duration", str(fare_attribute.transfer_duration))
            tree = ET.ElementTree(root)
            tree.write(os.path.join(parsedpath, "fare_attributes.xml"), xml_declaration=True, encoding='utf-8', method="xml")

            #fare_rules.txt
            root = ET.Element("{http://gtfs.bigbluebus.com/gtfs.xsd}gtfs", { "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation" : "http://gtfs.bigbluebus.com/ gtfs.xsd" })
            fare_rules = ET.SubElement(root, "{http://gtfs.bigbluebus.com/gtfs.xsd}fare_rules")
            for fare_attribute in schedule.GetFareAttributeList():
                for fare_rule in fare_attribute.GetFareRuleList():
                    item = ET.SubElement(fare_rules, "{http://gtfs.bigbluebus.com/gtfs.xsd}fare_rule", {"fare_id" : fare_attribute.fare_id })
                    if fare_rule.route_id:
                        item.set("route_id", fare_rule.route_id)
                    if fare_rule.origin_id is not None:
                        item.set("origin_id", fare_rule.origin_id)
                    if fare_rule.destination_id is not None:
                        item.set("destination_id", fare_rule.destination_id)
                    if fare_rule.contains_id is not None:
                        item.set("contains_id", fare_rule.contains_id)
            tree = ET.ElementTree(root)
            tree.write(os.path.join(parsedpath, "fare_rules.xml"), xml_declaration=True, encoding='utf-8', method="xml")

            #shapes.txt
            root = ET.Element("{http://gtfs.bigbluebus.com/gtfs.xsd}gtfs", { "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation" : "http://gtfs.bigbluebus.com/ gtfs.xsd" })
            shapes = ET.SubElement(root, "{http://gtfs.bigbluebus.com/gtfs.xsd}shapes")
            for shape in schedule.GetShapeList():
                item = ET.SubElement(shapes, "{http://gtfs.bigbluebus.com/gtfs.xsd}shape", { "shape_id" : shape.shape_id })
                for point in shape.points:
                    ET.SubElement(item, "{http://gtfs.bigbluebus.com/gtfs.xsd}shape_pt", { "shape_pt_lat" : str(point[0]), "shape_pt_lon" : str(point[1]) })
            tree = ET.ElementTree(root)
            tree.write(os.path.join(parsedpath, "shapes.xml"), xml_declaration=True, encoding='utf-8', method="xml")
            


            #export gis files in geojson

            #export distinct traces with route information
            tripList = schedule.GetTripList()
            features = []
            shapeList = sorted(tripList, key=lambda item: item.shape_id)
            directionList = sorted(shapeList, key=lambda item: item.direction_id)
            routeList = sorted(directionList, key=lambda item: item.route_id)
            for route_id, directionList in itertools.groupby(routeList, key=lambda item: item.route_id):
                trip_route = next(directionList)
                route = schedule.GetRoute(trip_route.route_id)
                for direction_id, shapeList in itertools.groupby(directionList, key=lambda item: item.direction_id):
                    trip_direction = next(shapeList)
                    lines = [[]]
                    previousSegments = [[]]
                    currentLine = 0
                    drawingLine = False
                    for shape_id, tripList in itertools.groupby(shapeList, key=lambda item: item.shape_id):
                        trip = next(tripList)
                        shape = schedule.GetShape(trip.shape_id)
                        trace = [[point[1], point[0]] for point in shape.points]
                        for pointIndex, point in enumerate(trace):
                            if pointIndex == 0:
                                pointEnd = point
                            else:
                                pointStart = pointEnd
                                pointEnd = point
                                segment = [pointStart, pointEnd]
                                if segment in previousSegments:
                                    if drawingLine:
                                        currentLine += 1
                                        lines.append([])
                                        drawingLine = False
                                else: # create this line
                                    if drawingLine: # continue line
                                        lines[currentLine].append(pointEnd)
                                    else: # begin line
                                        lines[currentLine].append(pointStart)
                                        lines[currentLine].append(pointEnd)
                                        drawingLine = True
                                    previousSegments.append(segment)
                        if drawingLine:
                            currentLine += 1
                            lines.append([])
                            drawingLine = False
                    feature = {"type": "Feature", "properties": { "route_id" : route.route_id, "direction_id" : trip.direction_id, "route_color" : route.route_color }, "geometry" : { "type": "MultiLineString","coordinates": [[[point[0], point[1]] for point in line] for line in lines] } }
                    features.append(feature)
            forJson = {"type": "FeatureCollection","crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } }, "features": features }
            json.dump(forJson, open(os.path.join(parsedpath, "traces.geojson"),"w"))

            #export shapes with route information
            tripList = schedule.GetTripList()
            features = []
            sortedTrips = sorted(tripList, key=lambda item: item.shape_id)
            for shape_id, trips in itertools.groupby(sortedTrips, key=lambda item: item.shape_id):
                trip = next(trips)
                route = schedule.GetRoute(trip.route_id)
                shape = schedule.GetShape(shape_id)
                feature = {"type": "Feature", "properties": { "shape_id" : shape.shape_id, "direction_id" : trip.direction_id, "trip_headsign" : trip.trip_headsign, "route_short_name" : route.route_short_name, "route_long_name" : route.route_long_name, "route_color" : route.route_color }, "geometry" : { "type": "LineString","coordinates": [[point[1], point[0]] for point in shape.points] } }
                features.append(feature)
            forJson = {"type": "FeatureCollection","crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } }, "features": features }
            json.dump(forJson, open(os.path.join(parsedpath, "shapes.geojson"),"w"))

            #export stops
            stopList = schedule.GetStopList()
            features = []
            for stop in stopList:
                feature = {"type": "Feature", "properties": { "stop_id" : stop.stop_id, "stop_code": stop.stop_code, "stop_name" : stop.stop_name, "stop_desc" : stop.stop_desc}, "geometry" : { "type" : "Point", "coordinates" : [stop.stop_lon, stop.stop_lat] } }
                features.append(feature)
            forJson = {"type": "FeatureCollection","crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } }, "features": features }
            json.dump(forJson, open(os.path.join(parsedpath, "stops.geojson"),"w"))



            #export gis files in kml

            ET.register_namespace("","http://www.opengis.net/kml/2.2")

            #export shapes with route information
            kml = ET.Element("{http://www.opengis.net/kml/2.2}kml")
            document = ET.SubElement(kml, "{http://www.opengis.net/kml/2.2}Document", {"id":"root_doc"})
            schema = ET.SubElement(document, "{http://www.opengis.net/kml/2.2}Schema", {"name":"shapes", "id":"shapes"})
            ET.SubElement(schema,"{http://www.opengis.net/kml/2.2}SimpleField", {"name":"shape_id", "type":"string"})
            ET.SubElement(schema,"{http://www.opengis.net/kml/2.2}SimpleField", {"name":"direction_id", "type":"string"})
            ET.SubElement(schema,"{http://www.opengis.net/kml/2.2}SimpleField", {"name":"trip_headsign", "type":"string"})
            ET.SubElement(schema,"{http://www.opengis.net/kml/2.2}SimpleField", {"name":"route_short_name", "type":"string"})
            ET.SubElement(schema,"{http://www.opengis.net/kml/2.2}SimpleField", {"name":"route_long_name", "type":"string"})
            ET.SubElement(schema,"{http://www.opengis.net/kml/2.2}SimpleField", {"name":"route_color", "type":"string"})
            folder = ET.SubElement(document, "{http://www.opengis.net/kml/2.2}Folder")
            ET.SubElement(folder,"{http://www.opengis.net/kml/2.2}name").text = "shapes"
            tripList = schedule.GetTripList()
            sortedTrips = sorted(tripList, key=lambda item: item.shape_id)
            for shape_id, trips in itertools.groupby(sortedTrips, key=lambda item: item.shape_id):
                trip = next(trips)
                route = schedule.GetRoute(trip.route_id)
                shape = schedule.GetShape(shape_id)
                coordinate_list = [(longitude, latitude) for (latitude, longitude, distance) in shape.points]
                coordinate_str_list = ["%f,%f" % t for t in coordinate_list]
                placemark = ET.SubElement(folder, "{http://www.opengis.net/kml/2.2}Placemark")
                name = ET.SubElement(placemark, "{http://www.opengis.net/kml/2.2}name").text = shape.shape_id
                style = ET.SubElement(placemark, "{http://www.opengis.net/kml/2.2}Style")
                linestyle = ET.SubElement(style, "{http://www.opengis.net/kml/2.2}LineStyle")
                ET.SubElement(linestyle, "{http://www.opengis.net/kml/2.2}color").text = "FF" + route.route_color
                extendeddata = ET.SubElement(placemark, "{http://www.opengis.net/kml/2.2}ExtendedData")
                schemadata = ET.SubElement(extendeddata, "{http://www.opengis.net/kml/2.2}SchemaData", {"schemaUrl": "#shapes"})
                ET.SubElement(schemadata,"{http://www.opengis.net/kml/2.2}SimpleData", {"name":"shape_id"}).text = shape.shape_id
                ET.SubElement(schemadata,"{http://www.opengis.net/kml/2.2}SimpleData", {"name":"direction_id"}).text = trip.direction_id
                ET.SubElement(schemadata,"{http://www.opengis.net/kml/2.2}SimpleData", {"name":"trip_headsign"}).text = trip.trip_headsign
                ET.SubElement(schemadata,"{http://www.opengis.net/kml/2.2}SimpleData", {"name":"route_short_name"}).text = route.route_short_name
                ET.SubElement(schemadata,"{http://www.opengis.net/kml/2.2}SimpleData", {"name":"route_long_name"}).text = route.route_long_name
                ET.SubElement(schemadata,"{http://www.opengis.net/kml/2.2}SimpleData", {"name":"route_color"}).text = route.route_color
                linestring = ET.SubElement(placemark,"{http://www.opengis.net/kml/2.2}LineString")
                ET.SubElement(linestring, "{http://www.opengis.net/kml/2.2}coordinates").text = " ".join(coordinate_str_list)
            tree = ET.ElementTree(kml)
            tree.write(os.path.join(parsedpath, "shapes.kml"), xml_declaration=True, encoding='utf-8', method="xml")

            #export stops
            kml = ET.Element("{http://www.opengis.net/kml/2.2}kml")
            document = ET.SubElement(kml, "{http://www.opengis.net/kml/2.2}Document", {"id":"root_doc"})
            schema = ET.SubElement(document, "{http://www.opengis.net/kml/2.2}Schema", {"name":"stops", "id":"stops"})
            ET.SubElement(schema,"{http://www.opengis.net/kml/2.2}SimpleField", {"name":"stop_id", "type":"string"})
            ET.SubElement(schema,"{http://www.opengis.net/kml/2.2}SimpleField", {"name":"stop_code", "type":"string"})
            ET.SubElement(schema,"{http://www.opengis.net/kml/2.2}SimpleField", {"name":"stop_name", "type":"string"})
            ET.SubElement(schema,"{http://www.opengis.net/kml/2.2}SimpleField", {"name":"stop_desc", "type":"string"})
            folder = ET.SubElement(document, "{http://www.opengis.net/kml/2.2}Folder")
            ET.SubElement(folder,"{http://www.opengis.net/kml/2.2}name").text = "stops"
            stopList = schedule.GetStopList()
            for stop in stopList:
                placemark = ET.SubElement(folder, "{http://www.opengis.net/kml/2.2}Placemark")
                name = ET.SubElement(placemark, "{http://www.opengis.net/kml/2.2}name").text = stop.stop_name
                extendeddata = ET.SubElement(placemark, "{http://www.opengis.net/kml/2.2}ExtendedData")
                schemadata = ET.SubElement(extendeddata, "{http://www.opengis.net/kml/2.2}SchemaData", {"schemaUrl": "#stops"})
                ET.SubElement(schemadata,"{http://www.opengis.net/kml/2.2}SimpleData", {"name":"stop_id"}).text = stop.stop_id
                ET.SubElement(schemadata,"{http://www.opengis.net/kml/2.2}SimpleData", {"name":"stop_code"}).text = stop.stop_code
                ET.SubElement(schemadata,"{http://www.opengis.net/kml/2.2}SimpleData", {"name":"stop_name"}).text = stop.stop_name
                ET.SubElement(schemadata,"{http://www.opengis.net/kml/2.2}SimpleData", {"name":"stop_desc"}).text = stop.stop_desc
                point = ET.SubElement(placemark,"{http://www.opengis.net/kml/2.2}Point")
                ET.SubElement(point, "{http://www.opengis.net/kml/2.2}coordinates").text = '%.6f,%.6f' % (stop.stop_lon, stop.stop_lat)
            tree = ET.ElementTree(kml)
            tree.write(os.path.join(parsedpath, "stops.kml"), xml_declaration=True, encoding='utf-8', method="xml")



            #export gis files in shapefile format and save in ZIP file
            prj = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]'

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

        previous_mtime = currentzipstat.st_mtime
    else:
        sleep(60)
    

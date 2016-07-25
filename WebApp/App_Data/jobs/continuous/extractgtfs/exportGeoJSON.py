import itertools
import json
import os

def process(schedule, parsedpath):

    print("traces.geojson")
    #export distinct traces with route, service, and direction information
    tripList = schedule.GetTripList()
    features = []
    shapeList = sorted(tripList, key=lambda item: item.shape_id)
    directionList = sorted(shapeList, key=lambda item: item.direction_id)
    serviceList = sorted(directionList, key=lambda item: item.service_id)
    routeList = sorted(serviceList, key=lambda item: item.route_id)
    for route_id, serviceList in itertools.groupby(routeList, key=lambda item: item.route_id):
        #print(route_id)
        route = schedule.GetRoute(route_id)
        for service_id, directionList in itertools.groupby(serviceList, key=lambda item: item.service_id):
            #print("\t" + service_id)
            service = schedule.GetServicePeriod(service_id)
            if service.day_of_week[0] | service.day_of_week[1] | service.day_of_week[2] | service.day_of_week[3] | service.day_of_week[4] | service.day_of_week[5] | service.day_of_week[6]:
                for direction_id, shapeList in itertools.groupby(directionList, key=lambda item: item.direction_id):
                    #print("\t\t" + direction_id)
                    lines = [[]]
                    previousSegments = [[]]
                    currentLine = 0
                    drawingLine = False
                    for shape_id, tripList in itertools.groupby(shapeList, key=lambda item: item.shape_id):
                        #print("\t\t\t" + shape_id)
                        shape = schedule.GetShape(shape_id)
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
                    feature = {"type": "Feature", "properties": { "route_id" : route.route_id, "service_id" : service_id, "direction_id" : direction_id, "route_color" : route.route_color }, "geometry" : { "type": "MultiLineString","coordinates": [[[point[0], point[1]] for point in line] for line in lines] } }
                    features.append(feature)
    forJson = {"type": "FeatureCollection","crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } }, "features": features }
    json.dump(forJson, open(os.path.join(parsedpath, "traces.geojson"),"w"))

    print("shapes.geojson")
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

    print("stops.geojson")
    #export stops
    stopList = schedule.GetStopList()
    features = []
    for stop in stopList:
        feature = {"type": "Feature", "properties": { "stop_id" : stop.stop_id, "stop_code": stop.stop_code, "stop_name" : stop.stop_name, "stop_desc" : stop.stop_desc}, "geometry" : { "type" : "Point", "coordinates" : [stop.stop_lon, stop.stop_lat] } }
        features.append(feature)
    forJson = {"type": "FeatureCollection","crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } }, "features": features }
    json.dump(forJson, open(os.path.join(parsedpath, "stops.geojson"),"w"))


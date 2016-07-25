import os
import xml.etree.cElementTree as ET

import transitfeed

def process(schedule, parsedpath):
    ET.register_namespace("","http://gtfs.bigbluebus.com/gtfs.xsd")
    ET.register_namespace("xsi","http://www.w3.org/2001/XMLSchema-instance")

    print("agency.xml")
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

    print("stops.xml")
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

    print("routes.xml")
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

    print("trips.xml")
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

    print("stop_times.xml")
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

    print("calendar.xml")
    root = ET.Element("{http://gtfs.bigbluebus.com/gtfs.xsd}gtfs", { "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation" : "http://gtfs.bigbluebus.com/ gtfs.xsd" })
    calendar = ET.SubElement(root, "{http://gtfs.bigbluebus.com/gtfs.xsd}calendar")
    for servicePeriod in schedule.GetServicePeriodList():
        item = ET.SubElement(calendar, "{http://gtfs.bigbluebus.com/gtfs.xsd}service", {"service_id" : servicePeriod.service_id, "monday" : str(servicePeriod.monday), "tuesday" : str(servicePeriod.tuesday), "wednesday" : str(servicePeriod.wednesday), "thursday" : str(servicePeriod.thursday), "friday" : str(servicePeriod.friday), "saturday" : str(servicePeriod.saturday), "sunday" : str(servicePeriod.sunday), "start_date" : servicePeriod.start_date, "end_date" : servicePeriod.end_date })
    tree = ET.ElementTree(root)
    tree.write(os.path.join(parsedpath, "calendar.xml"), xml_declaration=True, encoding='utf-8', method="xml")

    print("calendar_dates.xml")
    root = ET.Element("{http://gtfs.bigbluebus.com/gtfs.xsd}gtfs", { "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation" : "http://gtfs.bigbluebus.com/ gtfs.xsd" })
    calendar_dates = ET.SubElement(root, "{http://gtfs.bigbluebus.com/gtfs.xsd}calendar_dates")
    calendar = transitfeed.ServicePeriod()
    for calendar in schedule.GetServicePeriodList():
        for calendar_date in calendar.GetCalendarDatesFieldValuesTuples():
            item = ET.SubElement(calendar_dates, "{http://gtfs.bigbluebus.com/gtfs.xsd}calendar_date", { "service_id" : calendar_date[0], "date" : calendar_date[1], "exception_type" : calendar_date[2] })
    tree = ET.ElementTree(root)
    tree.write(os.path.join(parsedpath, "calendar_dates.xml"), xml_declaration=True, encoding='utf-8', method="xml")

    print("fare_attributes.xml")
    root = ET.Element("{http://gtfs.bigbluebus.com/gtfs.xsd}gtfs", { "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation" : "http://gtfs.bigbluebus.com/ gtfs.xsd" })
    fare_attributes = ET.SubElement(root, "{http://gtfs.bigbluebus.com/gtfs.xsd}fare_attributes")
    for fare_attribute in schedule.GetFareAttributeList():
        item = ET.SubElement(fare_attributes, "{http://gtfs.bigbluebus.com/gtfs.xsd}fare_attribute", {"fare_id" : fare_attribute.fare_id, "price" : str(fare_attribute.price), "currency_type" : str(fare_attribute.currency_type), "payment_method" : str(fare_attribute.payment_method), "transfers" : str(fare_attribute.transfers) })
        if fare_attribute.transfer_duration:
            item.set("transfer_duration", str(fare_attribute.transfer_duration))
    tree = ET.ElementTree(root)
    tree.write(os.path.join(parsedpath, "fare_attributes.xml"), xml_declaration=True, encoding='utf-8', method="xml")

    print("fare_rules.xml")
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

    print("shapes.xml")
    root = ET.Element("{http://gtfs.bigbluebus.com/gtfs.xsd}gtfs", { "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation" : "http://gtfs.bigbluebus.com/ gtfs.xsd" })
    shapes = ET.SubElement(root, "{http://gtfs.bigbluebus.com/gtfs.xsd}shapes")
    for shape in schedule.GetShapeList():
        item = ET.SubElement(shapes, "{http://gtfs.bigbluebus.com/gtfs.xsd}shape", { "shape_id" : shape.shape_id })
        for point in shape.points:
            ET.SubElement(item, "{http://gtfs.bigbluebus.com/gtfs.xsd}shape_pt", { "shape_pt_lat" : str(point[0]), "shape_pt_lon" : str(point[1]) })
    tree = ET.ElementTree(root)
    tree.write(os.path.join(parsedpath, "shapes.xml"), xml_declaration=True, encoding='utf-8', method="xml")
            

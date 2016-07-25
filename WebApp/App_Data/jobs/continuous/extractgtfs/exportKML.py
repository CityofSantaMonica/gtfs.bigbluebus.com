import itertools
import os
import xml.etree.cElementTree as ET

def process(schedule, parsedpath):

    ET.register_namespace("","http://www.opengis.net/kml/2.2")

    print("shapes.kml")
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

    print("stops.kml")
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


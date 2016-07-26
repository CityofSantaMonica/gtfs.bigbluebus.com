import os
import time
import xml.etree.cElementTree as ET

class RSSItem:
    def __init__(self, path, title, link, description):
        self.title = title
        self.link = link
        stat = os.stat(path)
        self.pubDate = stat.st_mtime
        self.description = description

class RSS:
    def __init__(self, rsspath):
        self.items = []
        self.rsspath = rsspath

    def add(self, item):
        self.items.append(item)

    def addTables(self, parsedpath, extension):
        self.add(RSSItem(os.path.join(parsedpath, "agency." + extension),"agency." + extension, "parsed/agency." + extension, "One or more transit agencies that provide the data in this feed."))
        self.add(RSSItem(os.path.join(parsedpath, "stops." + extension), "stops." + extension, "parsed/stops." + extension, "Individual locations where vehicles pick up or drop off passengers."))
        self.add(RSSItem(os.path.join(parsedpath, "routes." + extension), "routes." + extension, "parsed/routes." + extension, "Transit routes. A route is a group of trips that are displayed to riders as a single service."))
        self.add(RSSItem(os.path.join(parsedpath, "trips." + extension), "trips." + extension, "parsed/trips." + extension, "Trips for each route. A trip is a sequence of two or more stops that occurs at specific time."))
        self.add(RSSItem(os.path.join(parsedpath, "stop_times." + extension), "stop_times." + extension, "parsed/stop_times." + extension, "Times that a vehicle arrives at and departs from individual stops for each trip."))
        self.add(RSSItem(os.path.join(parsedpath, "calendar." + extension), "calendar." + extension, "parsed/calendar." + extension, "Dates for service IDs using a weekly schedule. Specify when service starts and ends, as well as days of the week where service is available."))
        self.add(RSSItem(os.path.join(parsedpath, "calendar_dates." + extension), "calendar_dates." + extension, "parsed/calendar_dates." + extension, "Exceptions for the service IDs defined in the calendar.txt file. If calendar_dates.txt includes ALL dates of service, this file may be specified instead of calendar.txt."))
        self.add(RSSItem(os.path.join(parsedpath, "fare_attributes." + extension), "fare_attributes." + extension, "parsed/fare_attributes." + extension, "Fare information for a transit organization's routes."))
        self.add(RSSItem(os.path.join(parsedpath, "fare_rules." + extension), "fare_rules." + extension, "parsed/fare_rules." + extension, "Rules for applying fare information for a transit organization's routes."))
        self.add(RSSItem(os.path.join(parsedpath, "shapes." + extension), "shapes." + extension, "parsed/shapes." + extension, "Rules for drawing lines on a map to represent a transit organization's routes."))

    def addGIS(self, parsedpath, extension):
        self.add(RSSItem(os.path.join(parsedpath, "shapes." + extension), "shapes." + extension, "parsed/shapes." + extension, "Rules for drawing lines on a map to represent a transit organization's routes."))
        self.add(RSSItem(os.path.join(parsedpath, "stops." + extension), "stops." + extension, "parsed/stops." + extension, "Individual locations where vehicles pick up or drop off passengers."))

    def save(self):
        rss = ET.Element('rss', {'version': '2.0'})
        channel = ET.SubElement(rss, "channel")
        ET.SubElement(channel, 'title').text = 'Big Blue Bus GTFS'
        for item in self.items:
            itemroot = ET.SubElement(channel, 'item')
            ET.SubElement(itemroot, 'title').text = item.title
            ET.SubElement(itemroot, 'link').text = "http://gtfs.bigbluebus.com/" + item.link
            ET.SubElement(itemroot, 'pubDate').text = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(item.pubDate))
            ET.SubElement(itemroot, 'description').text = item.description
        tree = ET.ElementTree(rss)
        tree.write(self.rsspath, xml_declaration=True, encoding='utf-8', method='xml')




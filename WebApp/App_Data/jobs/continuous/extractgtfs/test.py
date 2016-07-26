import os
from time import sleep
import zipfile

import exportJSON
import exportXML
import exportGeoJSON
import exportKML
import exportZIP
import RSS

import transitfeed

parsedpath = "../../../../parsed"
currentzippath = "../../../../current.zip"
rsspath = "../../../../rss.xml"
previous_mtime = 0

if not os.path.exists(parsedpath):
    os.makedirs(parsedpath)

if zipfile.is_zipfile(currentzippath):

    rss = RSS.RSS(rsspath)
    rss.add(RSS.RSSItem(currentzippath, "current.zip", "current.zip", "Current static GTFS data"))

    print("loading GTFS")
    #load gtfs from zip file
    schedule = transitfeed.Schedule()
    schedule.Load(currentzippath)

    print("exporting CSV")
    # export gtfs as csv
    currentzip = zipfile.ZipFile(currentzippath,'r')
    currentzip.extractall(parsedpath)
    rss.addTables(parsedpath, "txt")

    sleep(2)

    exportJSON.process(schedule, parsedpath)
    rss.addTables(parsedpath, "json")

    sleep(2)

    exportXML.process(schedule, parsedpath)
    rss.addTables(parsedpath, "xml")

    sleep(2)

    exportGeoJSON.process(schedule, parsedpath)
    rss.addGIS(parsedpath, "geojson")

    sleep(2)

    exportKML.process(schedule, parsedpath)
    rss.addGIS(parsedpath, "kml")

    sleep(2)

    exportZIP.process(schedule, parsedpath)
    rss.addGIS(parsedpath, "zip")

    rss.save()

import os
from time import sleep
import zipfile

import exportJSON
import exportXML
import exportGeoJSON
import exportKML
import exportZIP

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

            print("loading GTFS")
            #load gtfs from zip file
            schedule = transitfeed.Schedule()
            schedule.Load(currentzippath)

            print("exporting CSV")
            # export gtfs as csv
            currentzip = zipfile.ZipFile(currentzippath,'r')
            currentzip.extractall(parsedpath)

            sleep(2)

            exportJSON.process(schedule, parsedpath)

            sleep(2)

            exportXML.process(schedule, parsedpath)

            sleep(2)

            exportGeoJSON.process(schedule, parsedpath)

            sleep(2)

            exportKML.process(schedule, parsedpath)

            sleep(2)

            exportZIP.process(schedule, parsedpath)

        previous_mtime = currentzipstat.st_mtime
    else:
        sleep(60)
    

# Parse GTFS file

This Python file uses the [transitfeed](https://github.com/google/transitfeed) library from [Google](https://github.com/google) and the [pyshp](https://github.com/GeospatialPython/pyshp) library from [GeospatialPython](https://github.com/GeospatialPython).

[run.py](https://github.com/CityofSantaMonica/gtfs.bigbluebus.com/blob/master/App_Data/jobs/continuous/extractgtfs/run.py) is a continously running web job for [gtfs.bigbluebus.com](http://gtfs.bigbluebus.com/). It responds to updates to the current GTFS file (current.zip) and parses it to produce CSV, JSON, GeoJSON, KML, and Shapefiles.

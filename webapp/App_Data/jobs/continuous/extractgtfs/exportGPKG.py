import os
import sqlite3


# import transitfeed

def process(schedule, parsedpath):
    connection = sqlite3.connect(os.path.join(parsedpath, "gtfs.gpkg"))
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = cursor.fetchall()
    tablenames = [row[0] for row in rows]

    print("create GPKG")

    if "gpkg_spatial_ref_sys" not in tablenames:
        cursor.execute("CREATE TABLE gpkg_spatial_ref_sys "
                       "(srs_name TEXT NOT NULL,"
                       "srs_id INTEGER NOT NULL PRIMARY KEY,"
                       "organization TEXT NOT NULL,"
                       "organization_coordsys_id INTEGER NOT NULL,"
                       "definition  TEXT NOT NULL,"
                       "description TEXT);")
        cursor.executemany('INSERT INTO "gpkg_spatial_ref_sys" VALUES(?,?,?,?,?,?);', [
            ['Undefined cartesian SRS', -1, 'NONE', -1, 'undefined', 'undefined cartesian coordinate reference system'],
            ['Undefined geographic SRS', 0, 'NONE', 0, 'undefined', 'undefined geographic coordinate reference system'],
            ['WGS 84 geodetic', 4326, 'EPSG', 4326,
             'GEOGCS["WGS 84",'
             'DATUM["WGS_1984",'
             'SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],'
             'AUTHORITY["EPSG","6326"]],'
             'PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],'
             'UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],'
             'AUTHORITY["EPSG","4326"]]',
             'longitude/latitude coordinates in decimal degrees on the WGS 84 spheroid']
        ])

    if "gpkg_contents" not in tablenames:
        cursor.execute("CREATE TABLE gpkg_contents "
                       "(table_name TEXT NOT NULL PRIMARY KEY,"
                       "data_type TEXT NOT NULL,"
                       "identifier TEXT UNIQUE,"
                       "description TEXT DEFAULT '',"
                       "last_change DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ',CURRENT_TIMESTAMP)),"
                       "min_x DOUBLE,"
                       "min_y DOUBLE,"
                       "max_x DOUBLE,"
                       "max_y DOUBLE,"
                       "srs_id INTEGER,"
                       "CONSTRAINT fk_gc_r_srs_id FOREIGN KEY (srs_id) REFERENCES gpkg_spatial_ref_sys(srs_id));")
        cursor.executemany('INSERT INTO "gpkg_contents" VALUES(?,?,?,?,?,?,?,?,?,?);', [
            ['agency', 'aspatial', 'agency', '', '2016-07-30T20:22:18.000Z', None, None, None, None, 0],
            ['calendar', 'aspatial', 'calendar', '', '2016-07-30T20:25:07.000Z', None, None, None, None, 0],
            ['calendar_dates', 'aspatial', 'calendar_dates', '', '2016-07-30T20:49:13.000Z', None, None, None, None, 0],
            ['fare_attributes', 'aspatial', 'fare_attributes', '', '2016-07-30T20:51:09.000Z', None, None, None, None,
             0],
            ['fare_rules', 'aspatial', 'fare_rules', '', '2016-07-30T20:53:38.000Z', None, None, None, None, 0],
            ['feed_info', 'aspatial', 'feed_info', '', '2016-07-30T20:56:04.000Z', None, None, None, None, 0],
            ['frequencies', 'aspatial', 'frequencies', '', '2016-07-30T20:57:56.000Z', None, None, None, None, 0],
            ['routes', 'aspatial', 'routes', '', '2016-07-30T21:00:12.000Z', None, None, None, None, 0],
            ['shapes', 'features', 'shapes', '', '2016-07-30T21:02:01.000Z', None, None, None, None, 4326],
            ['stops', 'features', 'stops', '', '2016-07-30T21:04:37.000Z', None, None, None, None, 4326],
            ['stop_times', 'aspatial', 'stop_times', '', '2016-07-30T21:07:14.000Z', None, None, None, None, 0],
            ['transfers', 'aspatial', 'transfers', '', '2016-07-30T21:08:37.000Z', None, None, None, None, 0],
            ['trips', 'aspatial', 'trips', '', '2016-07-30T21:10:10.000Z', None, None, None, None, 0]
        ])

    if "gpkg_geometry_columns" not in tablenames:
        cursor.execute("CREATE TABLE gpkg_geometry_columns "
                       "(table_name TEXT NOT NULL,"
                       "column_name TEXT NOT NULL,"
                       "geometry_type_name TEXT NOT NULL,"
                       "srs_id INTEGER NOT NULL,"
                       "z TINYINT NOT NULL,"
                       "m TINYINT NOT NULL,"
                       "CONSTRAINT pk_geom_cols PRIMARY KEY (table_name, column_name),"
                       "CONSTRAINT uk_gc_table_name UNIQUE (table_name),"
                       "CONSTRAINT fk_gc_tn FOREIGN KEY (table_name) REFERENCES gpkg_contents(table_name),"
                       "CONSTRAINT fk_gc_srs FOREIGN KEY (srs_id) REFERENCES gpkg_spatial_ref_sys (srs_id));")
        cursor.executemany('INSERT INTO "gpkg_geometry_columns" VALUES(?,?,?,?,?,?);', [
            ['shapes', 'geometry', 'POINT', 4326, 0, 0],
            ['stops', 'geometry', 'POINT', 4326, 0, 0]
        ])
    if "gpkg_tile_matrix_set" not in tablenames:
        cursor.execute("CREATE TABLE gpkg_tile_matrix_set "
                       "(table_name TEXT NOT NULL PRIMARY KEY,"
                       "srs_id INTEGER NOT NULL,"
                       "min_x DOUBLE NOT NULL,"
                       "min_y DOUBLE NOT NULL,"
                       "max_x DOUBLE NOT NULL,"
                       "max_y DOUBLE NOT NULL,"
                       "CONSTRAINT fk_gtms_table_name FOREIGN KEY (table_name) REFERENCES gpkg_contents(table_name),"
                       "CONSTRAINT fk_gtms_srs FOREIGN KEY (srs_id) REFERENCES gpkg_spatial_ref_sys (srs_id));")
    if "gpkg_tile_matrix" not in tablenames:
        cursor.execute("CREATE TABLE gpkg_tile_matrix "
                       "(table_name TEXT NOT NULL,"
                       "zoom_level INTEGER NOT NULL,"
                       "matrix_width INTEGER NOT NULL,"
                       "matrix_height INTEGER NOT NULL,"
                       "tile_width INTEGER NOT NULL,"
                       "tile_height INTEGER NOT NULL,"
                       "pixel_x_size DOUBLE NOT NULL,"
                       "pixel_y_size DOUBLE NOT NULL,"
                       "CONSTRAINT pk_ttm PRIMARY KEY (table_name, zoom_level),"
                       "CONSTRAINT fk_tmm_table_name FOREIGN KEY (table_name) REFERENCES gpkg_contents(table_name));")
    if "gpkg_metadata" not in tablenames:
        cursor.execute("CREATE TABLE gpkg_metadata "
                       "(id INTEGER CONSTRAINT m_pk PRIMARY KEY ASC NOT NULL UNIQUE,"
                       "md_scope TEXT NOT NULL DEFAULT 'dataset',"
                       "md_standard_uri TEXT NOT NULL,"
                       "mime_type TEXT NOT NULL DEFAULT 'text/xml',"
                       "metadata TEXT NOT NULL);")
    if "gpkg_metadata_reference" not in tablenames:
        cursor.execute("CREATE TABLE gpkg_metadata_reference "
                       "(reference_scope TEXT NOT NULL,"
                       "table_name TEXT,column_name TEXT,"
                       "row_id_value INTEGER,"
                       "timestamp DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),"
                       "md_file_id INTEGER NOT NULL,md_parent_id INTEGER,"
                       "CONSTRAINT crmr_mfi_fk FOREIGN KEY (md_file_id) REFERENCES gpkg_metadata(id),"
                       "CONSTRAINT crmr_mpi_fk FOREIGN KEY (md_parent_id) REFERENCES gpkg_metadata(id));")
    if "gpkg_extensions" not in tablenames:
        cursor.execute("CREATE TABLE gpkg_extensions "
                       "(table_name TEXT,"
                       "column_name TEXT,"
                       "extension_name TEXT NOT NULL,"
                       "definition TEXT NOT NULL,"
                       "scope TEXT NOT NULL,"
                       "CONSTRAINT ge_tce UNIQUE (table_name, column_name, extension_name));")
        cursor.executemany('INSERT INTO "gpkg_extensions" VALUES(?,?,?,?,?);', [
            [None, None, 'gdal_aspatial', 'http://gdal.org/geopackage_aspatial.html', 'read-write'],
            ['shapes', 'geometry', 'gpkg_rtree_index', 'GeoPackage 1.0 Specification Annex L', 'write-only'],
            ['stops', 'geometry', 'gpkg_rtree_index', 'GeoPackage 1.0 Specification Annex L', 'write-only']
        ])
    print("agency")
    if "agency" not in tablenames:
        cursor.execute("CREATE TABLE agency "
                       "(fid INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "agency_id TEXT,"
                       "agency_name TEXT,"
                       "agency_url TEXT,"
                       "agency_timezone TEXT,"
                       "agency_lang TEXT,"
                       "agency_phone TEXT,"
                       "agency_fare_url TEXT);")
    cursor.execute("DELETE FROM agency;")
    cursor.executemany("INSERT INTO "
                       "agency(agency_id,"
                       "agency_name,"
                       "agency_url,"
                       "agency_timezone,"
                       "agency_lang,"
                       "agency_phone,"
                       "agency_fare_url) "
                       "VALUES(?,?,?,?,?,?,?);",
                           [(agency.agency_id,
                             agency.agency_name,
                             agency.agency_url,
                             agency.agency_timezone,
                             agency.agency_lang,
                             agency.agency_phone,
                             agency.agency_fare_url) for agency in schedule.GetAgencyList()])
    if "calendar" not in tablenames:
        cursor.execute("CREATE TABLE calendar "
                       "(fid INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "service_id TEXT,"
                       "monday INTEGER,"
                       "tuesday INTEGER,"
                       "wednesday INTEGER,"
                       "thursday INTEGER,"
                       "friday INTEGER,"
                       "saturday INTEGER,"
                       "sunday INTEGER,"
                       "start_date DATE,"
                       "end_date DATE);")
    if "calendar_dates" not in tablenames:
        cursor.execute('CREATE TABLE calendar_dates '
                       '(fid INTEGER PRIMARY KEY AUTOINCREMENT,'
                       'service_id TEXT,'
                       '"date" DATE,'
                       'exception_type INTEGER);')
    if "fare_attributes" not in tablenames:
        cursor.execute("CREATE TABLE fare_attributes "
                       "(fid INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "fare_id TEXT,"
                       "price REAL,"
                       "currency_type TEXT,"
                       "payment_method INTEGER,"
                       "transfers INTEGER,"
                       "transfer_duration INTEGER);")
    if "fare_rules" not in tablenames:
        cursor.execute("CREATE TABLE fare_rules "
                       "(fid INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "fare_id TEXT,"
                       "route_id TEXT,"
                       "origin_id TEXT,"
                       "destination_id TEXT,"
                       "contains_id TEXT);")
    if "routes" not in tablenames:
        cursor.execute("CREATE TABLE routes "
                       "(fid INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "route_id TEXT,"
                       "agency_id TEXT,"
                       "route_short_name TEXT,"
                       "route_long_name TEXT,"
                       "route_desc TEXT,"
                       "route_type INTEGER,"
                       "route_url TEXT,"
                       "route_color TEXT,"
                       "route_text_color TEXT);")
    if "shapes" not in tablenames:
        cursor.execute("CREATE TABLE shapes "
                       "(fid INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "geometry POINT,"
                       "shape_id TEXT,"
                       "shape_pt_lat REAL,"
                       "shape_pt_lon REAL,"
                       "shape_pt_sequence INTEGER,"
                       "shape_dist_traveled REAL);")
    print("stops")
    if "stops" not in tablenames:
        cursor.execute("CREATE TABLE stops "
                       "(fid INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "geometry POINT,"
                       "stop_id TEXT,"
                       "stop_code TEXT,"
                       "stop_name TEXT,"
                       "stop_desc TEXT,"
                       "stop_lat REAL,"
                       "stop_lon REAL,"
                       "zone_id TEXT,"
                       "stop_url TEXT,"
                       "location_type INTEGER,"
                       "parent_station INTEGER,"
                       "stop_timezone TEXT,"
                       "wheelchair_boarding INTEGER);")
    cursor.execute("DELETE FROM stops;")
    cursor.executemany("INSERT INTO stops(geometry,"
                       "stop_id,"
                       "stop_code,"
                       "stop_name,"
                       "stop_desc,"
                       "stop_lat,"
                       "stop_lon,"
                       "zone_id,"
                       "stop_url,"
                       "location_type,"
                       "parent_station,"
                       "stop_timezone," 
                       "wheelchair_boarding) "
                       "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?);",
                       [("ST_PointFromText('POINT(" + str(stop.stop_lon) + " " + str(stop.stop_lat) + ")')",
                         stop.stop_id,
                         stop.stop_code,
                         stop.stop_name,
                         stop.stop_desc,
                         stop.stop_lat,
                         stop.stop_lon,
                         stop.zone_id,
                         stop.stop_url,
                         stop.location_type,
                         stop.parent_station,
                         stop.stop_timezone,
                         stop.wheelchair_boarding) for stop in schedule.GetStopList()])
    if "stop_times" not in tablenames:
        cursor.execute("CREATE TABLE stop_times "
                       "(fid INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "trip_id TEXT,"
                       "arrival_time TEXT,"
                       "departure_time TEXT,"
                       "stop_id TEXT,"
                       "stop_sequence INTEGER,"
                       "stop_headsign TEXT,"
                       "pickup_type INTEGER,"
                       "drop_off_type INTEGER,"
                       "shape_dist_traveled REAL,"
                       "timepoint INTEGER);")
    if "trips" not in tablenames:
        cursor.execute("CREATE TABLE trips "
                       "(fid INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "route_id TEXT,"
                       "service_id TEXT,"
                       "trip_id TEXT,"
                       "trip_headsign TEXT,"
                       "trip_short_name TEXT,"
                       "direction_id INTEGER,"
                       "block_id TEXT,"
                       "shape_id TEXT,"
                       "wheelchair_accessible INTEGER,"
                       "bikes_allowed INTEGER);")
    connection.commit()


        # forJson = {}
    # for agency in schedule.GetAgencyList():
    #     forJson[agency.agency_id] = {"agency_id" : agency.agency_id, "agency_name" : agency.agency_name, "agency_url" : agency.agency_url, "agency_timezone" : agency.agency_timezone, "agency_lang" : agency.agency_lang, "agency_phone" : agency.agency_phone, "agency_fare_url" : agency.agency_fare_url }
    # json.dump(forJson, open(os.path.join(parsedpath, "agency.json"),"w"))
    #
    # print("stops.json")
    # forJson = {}
    # for stop in schedule.GetStopList():
    #     forJson[stop.stop_id] = {"stop_id" : stop.stop_id, "stop_code" : stop.stop_code, "stop_name" : stop.stop_name, "stop_desc" : stop.stop_desc, "stop_lat" : stop.stop_lat, "stop_lon" : stop.stop_lon, "zone_id" : stop.zone_id, "stop_url" : stop.stop_url, "location_type" : stop.location_type, "parent_station" : stop.parent_station, "stop_timezone" : stop.stop_timezone, "wheelchair_boarding" : stop.wheelchair_boarding }
    # json.dump(forJson, open(os.path.join(parsedpath, "stops.json"),"w"))
    #
    # print("routes.json")
    # forJson = {}
    # for route in schedule.GetRouteList():
    #     forJson[route.route_id] = {"route_id" : route.route_id, "agency_id" : route.agency_id, "route_short_name" : route.route_short_name, "route_long_name" : route.route_long_name, "route_desc" : route.route_desc, "route_type" : route.route_type, "route_url" : route.route_url, "route_color" : route.route_color, "route_text_color" : route.route_text_color }
    # json.dump(forJson, open(os.path.join(parsedpath, "routes.json"),"w"))
    #
    # print("trips.json")
    # forJson = {}
    # for trip in schedule.GetTripList():
    #     forJson[trip.trip_id] = {"route_id" : trip.route_id, "service_id" : trip.service_id, "trip_id" : trip.trip_id, "trip_headsign" : trip.trip_headsign, "trip_short_name" : trip.trip_short_name, "direction_id" : trip.direction_id, "block_id" : trip.block_id, "shape_id" : trip.shape_id, "wheelchair_accessible" : trip.wheelchair_accessible, "bikes_allowed" : trip.bikes_allowed }
    # json.dump(forJson, open(os.path.join(parsedpath, "trips.json"),"w"))
    #
    # print("stop_times.json")
    # forJson = {}
    # for trip in schedule.GetTripList():
    #     stop_times = {}
    #     for stop_time in sorted(trip.GetStopTimes(), key=lambda item: item.stop_sequence):
    #         stop_times[stop_time.stop_sequence] = {"trip_id" : trip.trip_id, "arrival_time" : stop_time.arrival_time, "departure_time" : stop_time.departure_time, "stop_id" : stop_time.stop_id, "stop_sequence" : stop_time.stop_sequence, "stop_headsign" : stop_time.stop_headsign, "pickup_type" : stop_time.pickup_type, "drop_off_type" : stop_time.drop_off_type, "shape_dist_traveled" : stop_time.shape_dist_traveled, "timepoint" : stop_time.timepoint }
    #         forJson[trip.trip_id] = stop_times
    # json.dump(forJson, open(os.path.join(parsedpath, "stop_times.json"),"w"))
    #
    # print("calendar.json")
    # forJson = {}
    # for calendar in schedule.GetServicePeriodList():
    #     forJson[calendar.service_id] = {"service_id" : calendar.service_id, "monday" : calendar.monday, "tuesday" : calendar.tuesday, "wednesday" : calendar.wednesday, "thursday" : calendar.thursday, "friday" : calendar.friday, "saturday" : calendar.saturday, "sunday" : calendar.sunday, "start_date" : calendar.start_date, "end_date" : calendar.end_date }
    # json.dump(forJson, open(os.path.join(parsedpath, "calendar.json"),"w"))
    #
    # print("calendar_dates.json")
    # forJson = []
    # calendar = transitfeed.ServicePeriod()
    # for calendar in schedule.GetServicePeriodList():
    #     for calendar_date in calendar.GetCalendarDatesFieldValuesTuples():
    #         forJson.append({"service_id" : calendar_date[0], "date" : calendar_date[1], "exception_type" : calendar_date[2] })
    # json.dump(forJson, open(os.path.join(parsedpath, "calendar_dates.json"),"w"))
    #
    # print("fare_attributes.json")
    # forJson = {}
    # for fare_attribute in schedule.GetFareAttributeList():
    #     forJson[fare_attribute.fare_id] = {"fare_id" : fare_attribute.fare_id, "price" : fare_attribute.price, "currency_type" : fare_attribute.currency_type, "payment_method" : fare_attribute.payment_method, "transfers" : fare_attribute.transfers, "transfer_duration" : fare_attribute.transfer_duration }
    # json.dump(forJson, open(os.path.join(parsedpath, "fare_attributes.json"),"w"))
    #
    # print("fare_rules.json")
    # forJson = []
    # for fare_attribute in schedule.GetFareAttributeList():
    #     for fare_rule in fare_attribute.GetFareRuleList():
    #         forJson.append({"fare_id" : fare_attribute.fare_id, "route_id" : fare_rule.route_id, "origin_id" : fare_rule.origin_id, "destination_id" : fare_rule.destination_id, "contains_id" : fare_rule.contains_id })
    # json.dump(forJson, open(os.path.join(parsedpath, "fare_rules.json"),"w"))
    #
    # print("shapes.json")
    # forJson = {}
    # for shape in schedule.GetShapeList():
    #     forJson[shape.shape_id] = { "shape_id" : shape.shape_id, "points" : [ { "shape_pt_lat" : point[0], "shape_pt_lon" : point[1]} for point in shape.points  ] }
    # json.dump(forJson, open(os.path.join(parsedpath, "shapes.json"),"w"))

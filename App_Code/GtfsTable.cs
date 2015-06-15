using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Web;

/// <summary>
/// Summary description for GtfsTable
/// </summary>
public class GtfsTable
{
    public String Name { get; set; }
    public String Extension { get; set; }
    public String FileName { get { return Name + Extension; } }
    public String FilePath { get; set; }
    public String Description { get; set; }
    public String DocumentationUrl { get { return String.Format("https://developers.google.com/transit/gtfs/reference#{0}_fields", Name); } }
    public Boolean Exists { get; set; }
    public DateTime LastUpdateUtc { get; set; }

    public static IEnumerable<GtfsTable> GetAll(String extension, HttpServerUtility server)
    {
        var tables = new[]{
            new GtfsTable{ Name="agency", Description="One or more transit agencies that provide the data in this feed."},
            new GtfsTable{ Name="stops", Description="Individual locations where vehicles pick up or drop off passengers."},
            new GtfsTable{ Name="routes", Description="Transit routes. A route is a group of trips that are displayed to riders as a single service."},
            new GtfsTable{ Name="trips", Description="Trips for each route. A trip is a sequence of two or more stops that occurs at specific time."},
            new GtfsTable{ Name="stop_times", Description="Times that a vehicle arrives at and departs from individual stops for each trip."},
            new GtfsTable{ Name="calendar", Description="Dates for service IDs using a weekly schedule. Specify when service starts and ends, as well as days of the week where service is available."},
            new GtfsTable{ Name="calendar_dates", Description="Exceptions for the service IDs defined in the calendar.txt file. If calendar_dates.txt includes ALL dates of service, this file may be specified instead of calendar.txt."},
            new GtfsTable{ Name="fare_attributes", Description="Fare information for a transit organization's routes."},
            new GtfsTable{ Name="fare_rules", Description="Rules for applying fare information for a transit organization's routes."},
            new GtfsTable{ Name="shapes", Description="Rules for drawing lines on a map to represent a transit organization's routes."},
            new GtfsTable{ Name="feed_info", Description="Additional information about the feed itself, including publisher, version, and expiration information."}
        }.ToList();
        tables.ForEach(t => CheckTable(t, extension, server));
        return tables.Where(t => t.Exists);
    }
    private static void CheckTable(GtfsTable gtfsTable, String extension, HttpServerUtility server)
    {
        gtfsTable.FilePath = String.Format("/parsed/{0}{1}", gtfsTable.Name, extension);
        var fileInfo = new FileInfo(server.MapPath(gtfsTable.FilePath));
        gtfsTable.Extension = fileInfo.Extension;
        gtfsTable.Exists = fileInfo.Exists;
        gtfsTable.LastUpdateUtc = fileInfo.LastWriteTimeUtc;
    }
}
using System;
using System.Linq;
using System.Collections.Generic;
using System.IO;
using System.Web;

public class GtfsFile
{
    public string FileName { get; set; }
    public string Description { get; set; }
    public KeyValuePair<string, string> DocumentationUrl { get; set; }

    public DateTime LastUpdateUtc { get; set; }

    public static IEnumerable<GtfsFile> GetAll(HttpServerUtility server)
    {
        var files = new[] {
            new GtfsFile { 
                FileName = "current.zip",
                Description = "<p>The current static GTFS data. This file will always contain the current schedule period.</p><p>At the time of a schedule change, this file will contain both schedule periods merged together. Your software must use the date ranges in the calendar.txt table to select the correct trips based on date.</p>",
                DocumentationUrl = new KeyValuePair<string,string>("https://developers.google.com/transit/gtfs/", "GTFS")
            },
            new GtfsFile {
                FileName = "alerts.bin",
                Description = "GTFS-Realtime alert data. This file contains information about availability of stops and routes.",
                DocumentationUrl = new KeyValuePair<string,string>("https://developers.google.com/transit/gtfs-realtime/service-alerts", "GTFS-realtime Service Alerts")
            },
            new GtfsFile {
                FileName = "tripupdates.bin",
                Description = "GTFS-Realtime trip update data. This file contains information about the arrival times of current trips.",
                DocumentationUrl = new KeyValuePair<string,string>("https://developers.google.com/transit/gtfs-realtime/trip-updates", "GTFS-realtime Trip Updates")
            },
            new GtfsFile {
                FileName = "vehiclepositions.bin",
                Description = "GTFS-Realtime vehicle position data. This file contains the most recent latitude/longitude of vehicles assigned to current trips.",
                DocumentationUrl = new KeyValuePair<string,string>("https://developers.google.com/transit/gtfs-realtime/vehicle-positions", "GTFS-realtime Vehicle Positions")
            }
        }.ToList();

        files.ForEach(f => AssignLastUpdate(f, server));

        return files;
    }

    private static void AssignLastUpdate(GtfsFile gtfs, HttpServerUtility server)
    {
        gtfs.LastUpdateUtc = new FileInfo(server.MapPath(gtfs.FileName)).LastWriteTimeUtc;
    }
}

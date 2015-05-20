<%@ Page Language="C#" AutoEventWireup="true" CodeFile="default.aspx.cs" Inherits="_default" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    
    <title>Big Blue Bus GTFS Service</title>

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
    <link href="site.css" rel="stylesheet">
</head>
<body>
    <form id="form1" runat="server">
    <div class="container">
        <h1 class="page-header">Big Blue Bus GTFS Service</h1>
        <table class="table table-bordered table-striped">
            <thead>
                <tr>
                    <th>URL</th>
                    <th>Last Update</th>
                    <th>Description</th>
                    <th>Documentation</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>
                        <a href="current.zip">current.zip</a>
                    </td>
                    <td class="file-time"><%= CurrentLastUpdate.ToString(DateTimeFormat) %></td>
                    <td>
                        <p>The current static GTFS data. This file will always contain the current schedule period.</p>
                        <p>At the time of a schedule change, this file will contain both schedule periods merged together. Your software must use the date ranges in the calendar.txt table to select the correct trips based on date.</p>
                    </td>
                    <td><a href="https://developers.google.com/transit/gtfs/">GTFS</a></td>
                </tr>
                <tr>
                    <td>
                        <a href="alerts.bin">alerts.bin</a></td>
                    <td class="file-time"><%= AlertsLastUpdate.ToString(DateTimeFormat) %></td>
                    <td><p>GTFS-Realtime alert data. This file contains information about availability of stops and routes.</p></td>
                    <td><a href="https://developers.google.com/transit/gtfs-realtime/service-alerts">GTFS-realtime Service Alerts</a></td>
                </tr>
                <tr>
                    <td>
                        <a href="tripupdates.bin">tripupdates.bin</a></td>
                    <td class="file-time"><%= TripupdatesLastUpdate.ToString(DateTimeFormat) %></td>
                    <td><p>GTFS-Realtime trip update data. This file contains information about the arrival times of current trips.</p></td>
                    <td><a href="https://developers.google.com/transit/gtfs-realtime/trip-updates">GTFS-realtime Trip Updates</a></td>
                </tr>
                <tr>
                    <td>
                        <a href="vehiclepositions.bin">vehiclepositions.bin</a></td>
                    <td class="file-time"><%= VehiclepositionsLastUpdate.ToString(DateTimeFormat) %></td>
                    <td><p>GTFS-Realtime vehicle position data. This file contains the most recent latitude/longitude of vehicles assigned to current trips.</p></td>
                    <td><a href="https://developers.google.com/transit/gtfs-realtime/vehicle-positions">GTFS-realtime Vehicle Positions</a></td>
                </tr>
            </tbody>
        </table>
        <h2>Archive</h2>
        <p>Previous versions of our GTFS files may be downloaded from <a href="https://github.com/CityofSantaMonica/GTFS" target="_blank">GitHub</a>.</p>
    </div>
    </form>
</body>
</html>

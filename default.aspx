<%@ Page Language="C#" %>

<!DOCTYPE html>

<script runat="server">

    public DateTime currentLastUpdate
    {
        get
        {
            var fileInfo = new System.IO.FileInfo(Server.MapPath("current.zip"));
            return fileInfo.LastWriteTime;
        }
    }

    public DateTime alertsLastUpdate
    {
        get
        {
            var fileInfo = new System.IO.FileInfo(Server.MapPath("alerts.bin"));
            return fileInfo.LastWriteTime;
        }
    }

    public DateTime tripupdatesLastUpdate
    {
        get
        {
            var fileInfo = new System.IO.FileInfo(Server.MapPath("tripupdates.bin"));
            return fileInfo.LastWriteTime;
        }
    }

    public DateTime vehiclepositionsLastUpdate
    {
        get
        {
            var fileInfo = new System.IO.FileInfo(Server.MapPath("vehiclepositions.bin"));
            return fileInfo.LastWriteTime;
        }
    }
    
</script>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title>Big Blue Bus GTFS Service</title>
    <link href="site.css" rel="stylesheet" />
</head>
<body>
    <form id="form1" runat="server">
        <div>
            <h1>Big Blue Bus GTFS Service</h1>
            <table>
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
                        <td class="file-time"><%= currentLastUpdate.ToString("yyyy-MM-ddTHH:mm:ssZ") %></td>
                        <td>
                            <p>The current static GTFS data. This file will always contain the current schedule period.</p>
                            <p>At the time of a schedule change, this file will contain both schedule periods merged together. Your software must use the date ranges in the calendar.txt table to select the correct trips based on date.</p>
                        </td>
                        <td><a href="https://developers.google.com/transit/gtfs/">GTFS</a></td>
                    </tr>
                    <tr>
                        <td>
                            <a href="alerts.bin">alerts.bin</a></td>
                        <td class="file-time"><%= alertsLastUpdate.ToString("yyyy-MM-ddTHH:mm:ssZ") %></td>
                        <td><p>GTFS-Realtime alert data. This file contains information about availability of stops and routes.</p></td>
                        <td><a href="https://developers.google.com/transit/gtfs-realtime/service-alerts">GTFS-realtime Service Alerts</a></td>
                    </tr>
                    <tr>
                        <td>
                            <a href="tripupdates.bin">tripupdates.bin</a></td>
                        <td class="file-time"><%= tripupdatesLastUpdate.ToString("yyyy-MM-ddTHH:mm:ssZ") %></td>
                        <td><p>GTFS-Realtime trip update data. This file contains information about the arrival times of current trips.</p></td>
                        <td><a href="https://developers.google.com/transit/gtfs-realtime/trip-updates">GTFS-realtime Trip Updates</a></td>
                    </tr>
                    <tr>
                        <td>
                            <a href="vehiclepositions.bin">vehiclepositions.bin</a></td>
                        <td class="file-time"><%= vehiclepositionsLastUpdate.ToString("yyyy-MM-ddTHH:mm:ssZ") %></td>
                        <td><p>GTFS-Realtime vehicle position data. This file contains the most recent latitude/longitude of vehicles assigned to current trips.</p></td>
                        <td><a href="https://developers.google.com/transit/gtfs-realtime/vehicle-positions">GTFS-realtime Vehicle Positions</a></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </form>
    <h2>Archive</h2>
    <p>
        Previous versions of our GTFS files may be downloaded from <a href="https://github.com/CityofSantaMonica/GTFS">GitHub</a>.</p>
</body>
</html>

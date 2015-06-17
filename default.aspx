<%@ Page Title="" Language="C#" MasterPageFile="~/site.master" AutoEventWireup="true" CodeFile="default.aspx.cs" Inherits="_default" %>

<%@ Register Src="~/ParsedFileList.ascx" TagPrefix="uc1" TagName="ParsedFileList" %>

<asp:Content ID="Content1" ContentPlaceHolderID="HeadContentPlaceHolder" runat="Server">
    <script src="https://maps.googleapis.com/maps/api/js?v=3.exp"></script>
    <script src="https://googlemaps.github.io/js-map-label/src/maplabel-compiled.js"></script>
    <script src="javascript-protobuf/Long.js"></script>
    <script src="javascript-protobuf/ByteBufferAB.js"></script>
    <script src="javascript-protobuf/ProtoBuf.js"></script>
    <script src="javascript-protobuf/Example.js"></script>
</asp:Content>

<asp:Content ID="MainContent" ContentPlaceHolderID="MainContentPlaceHolder" runat="Server">
    <h1 class="page-header">Big Blue Bus GTFS Service</h1>
    <table class="table table-bordered table-striped table-responsive">
        <thead>
            <tr>
                <th>URL</th>
                <th>Last Update UTC</th>
                <th>Description</th>
                <th>Documentation</th>
            </tr>
        </thead>
        <tbody>
            <asp:Repeater ID="GTFSFileRepeater" runat="server" ItemType="GtfsFile">
                <ItemTemplate>
                    <tr>
                        <td>
                            <a href="<%#Item.FileName %>"><%#Item.FileName %></a>
                        </td>
                        <td class="file-time">
                            <span><%#Item.LastUpdateUtc.ToString(DateTimeFormat) %></span>
                        </td>
                        <td>
                            <%#Item.Description %>
                        </td>
                        <td>
                            <a href="<%#Item.DocumentationUrl.Key %>" target="_blank"><%#Item.DocumentationUrl.Value %></a>
                        </td>
                    </tr>
                </ItemTemplate>
            </asp:Repeater>
        </tbody>
    </table>
    <h2 id="livemap">Example Live Map</h2>
    <p>This map is example code for the developer community.</p>
    <p>The source code is available on <a href="https://github.com/CityofSantaMonica/gtfs.bigbluebus.com/tree/master/javascript-protobuf">GitHub</a></p>
    <ul>
        <li>Hover over bus (colored circle) for route, destination, bus number, and schedule adherance.</li>
        <li>Click on bus (colored circle) to display route<span id="scheduledstoptimesmessage" style="display: none"> and scheduled stop times</span>.</li>
        <li>Map refreshes every 30 seconds</li>
        <li>Busses update their locations in intervals of about 45 seconds</li>
    </ul>
    <div id="example-map" style="width: 100%; height: 480px"></div>
    <h2>Parsed Data Files</h2>
    <p>Each time the static GTFS file is updated (current.zip) the server will parse it into data files that can be accessed directly.</p>
    <h3>CSV files</h3>
    <uc1:ParsedFileList runat="server" id="ParsedFileListTXT" Extension=".txt" />
    <h3>JSON files</h3>
    <uc1:ParsedFileList runat="server" id="ParsedFileListJSON" Extension=".json" />
    <h2>GIS files</h2>
    <h3>GeoJSON files</h3>
    <uc1:ParsedFileList runat="server" id="ParsedFileListGeoJSON" Extension=".geojson" />
    <h3>KML files</h3>
    <uc1:ParsedFileList runat="server" id="ParsedFileListKML" Extension=".kml" />
    <h3>Shapefiles in ZIP</h3>
    <uc1:ParsedFileList runat="server" id="ParsedFileList1" Extension=".zip" />
</asp:Content>


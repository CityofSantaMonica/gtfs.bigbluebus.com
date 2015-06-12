<%@ Page Title="" Language="C#" MasterPageFile="~/site.master" AutoEventWireup="true" CodeFile="default.aspx.cs" Inherits="_default" %>

<asp:Content ID="Content1" ContentPlaceHolderID="HeadContentPlaceHolder" runat="Server">
    <script src="https://maps.googleapis.com/maps/api/js?v=3.exp"></script>
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
    <h2 id="livemap">Live Map</h2>
    <ul>
        <li>Hover over bus (colored circle) for route, bus number, and schedule adherance.</li>
        <li>Click on bus (colored circle) to display route</li>
        <li>Map refreshes every 20 seconds</li>
        <li>Busses update their locations in intervals of about 45 seconds</li>
    </ul>
    <div id="example-map" style="width: 100%; height: 480px"></div>
</asp:Content>


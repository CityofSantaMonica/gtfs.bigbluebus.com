<%@ Page Title="" Language="C#" MasterPageFile="~/site.master" AutoEventWireup="true" CodeFile="default.aspx.cs" Inherits="_default" %>

<%@ Register Src="~/ParsedFileList.ascx" TagPrefix="uc1" TagName="ParsedFileList" %>


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
                            <a href="<%# Item.DocumentationUrl.Key %>" target="_blank"><%# Item.DocumentationUrl.Value %></a>
                        </td>
                    </tr>
                </ItemTemplate>
            </asp:Repeater>
        </tbody>
    </table>
    <h2>CSV files</h2>
    <uc1:ParsedFileList runat="server" id="ParsedFileListTXT" Extension=".txt" />
    <h2>JSON files</h2>
    <uc1:ParsedFileList runat="server" id="ParsedFileListJSON" Extension=".json" />
    <h2>GeoJSON files</h2>
    <uc1:ParsedFileList runat="server" id="ParsedFileListGeoJSON" Extension=".geojson" />
</asp:Content>


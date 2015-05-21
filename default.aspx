<%@ Page Title="" Language="C#" MasterPageFile="~/site.master" AutoEventWireup="true" CodeFile="default.aspx.cs" Inherits="_default" %>

<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="Server">
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolder1" runat="Server">
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
</asp:Content>


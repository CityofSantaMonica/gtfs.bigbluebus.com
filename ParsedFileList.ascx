<%@ Control Language="C#" AutoEventWireup="true" CodeFile="ParsedFileList.ascx.cs" Inherits="ParsedFileList" %>
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
            <asp:Repeater ID="GTFSTableRepeater" runat="server" ItemType="GtfsTable">
                <ItemTemplate>
                    <tr>
                        <td>
                            <a href="<%# Item.FilePath %>"><%# Item.FileName %></a>
                        </td>
                        <td class="file-time">
                            <span><%# Item.LastUpdateUtc.ToString(DateTimeFormat) %></span>
                        </td>
                        <td>
                            <%# Item.Description %>
                        </td>
                        <td>
                            <a href="<%# Item.DocumentationUrl %>" target="_blank"><%# Item.Name %></a>
                        </td>
                    </tr>
                </ItemTemplate>
            </asp:Repeater>
        </tbody>
    </table>

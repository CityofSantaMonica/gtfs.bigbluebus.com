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
    <div class="navbar">
        <div class="container">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="/"><img src="BBB-logo.jpg" alt="Big Blue Bus GTFS Service" /></a>
            </div>
            <div id="navbar" class="collapse navbar-collapse">
              <ul class="nav nav-pills pull-right">
                  <asp:Repeater ID="NavBarRepeater" runat="server" ItemType="NavBarItem">
                      <ItemTemplate>
                          <li><a href="<%# Item.Url  %>" target="_blank"><%# Item.Text %></a></li>
                      </ItemTemplate>
                  </asp:Repeater>
              </ul>
            </div>
        </div>
    </div>
    <div class="container">
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
        <hr />
        <footer>
            &copy; <%=DateTime.Now.Year %> City of Santa Monica
        </footer>
    </div>
    </form>
    <script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
</body>
</html>

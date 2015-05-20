using System;

public partial class _default : System.Web.UI.Page
{
    public readonly string DateTimeFormat = "yyyy-MM-ddTHH:mm:ssZ";

    public DateTime CurrentLastUpdate
    {
        get
        {
            var fileInfo = new System.IO.FileInfo(Server.MapPath("current.zip"));
            return fileInfo.LastWriteTime;
        }
    }

    public DateTime AlertsLastUpdate
    {
        get
        {
            var fileInfo = new System.IO.FileInfo(Server.MapPath("alerts.bin"));
            return fileInfo.LastWriteTime;
        }
    }

    public DateTime TripupdatesLastUpdate
    {
        get
        {
            var fileInfo = new System.IO.FileInfo(Server.MapPath("tripupdates.bin"));
            return fileInfo.LastWriteTime;
        }
    }

    public DateTime VehiclepositionsLastUpdate
    {
        get
        {
            var fileInfo = new System.IO.FileInfo(Server.MapPath("vehiclepositions.bin"));
            return fileInfo.LastWriteTime;
        }
    }

    protected void Page_Load(object sender, EventArgs e)
    {

    }
}
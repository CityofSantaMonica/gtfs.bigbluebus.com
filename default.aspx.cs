using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class _default : System.Web.UI.Page
{
    public readonly string DateTimeFormat = "yyyy-MM-ddTHH:mm:ssZ";

    protected void Page_Load(object sender, EventArgs e)
    {
        GTFSFileRepeater.DataSource = GtfsFile.GetAll(Page.Server);
        GTFSFileRepeater.DataBind();
    }
}
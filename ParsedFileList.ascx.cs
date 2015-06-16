using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class ParsedFileList : System.Web.UI.UserControl
{
    public readonly string DateTimeFormat = "yyyy-MM-ddTHH:mm:ssZ";
    protected void Page_Load(object sender, EventArgs e)
    {
        GTFSTableRepeater.DataSource = GtfsTable.GetAll(Extension, Page.Server);
        GTFSTableRepeater.DataBind();
    }
    public String Extension { get; set; }
}
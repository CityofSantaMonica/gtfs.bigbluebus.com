using System;
using System.Linq;

public partial class _default : System.Web.UI.Page
{
    public readonly string DateTimeFormat = "yyyy-MM-ddTHH:mm:ssZ";

    protected void Page_Load(object sender, EventArgs e)
    {
        NavBarRepeater.DataSource = NavBarItem.GetAll();

        GTFSFileRepeater.DataSource = GtfsFile.GetAll(Page.Server);

        Page.DataBind();
    }
}
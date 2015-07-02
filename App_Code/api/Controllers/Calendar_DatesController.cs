using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Web.Http;

using api.Models;
using System.Web;

namespace api.Controllers
{
    public class Calendar_DatesController : ApiController
    {
        [Route("api/calendar_dates")]
        public IEnumerable<ViewModels.Calendar_Date> GetAllCalendar_Dates()
        {
            return new gtfs(HttpContext.Current).calendar_dates.Select(calendar_date => new ViewModels.Calendar_Date(calendar_date));
        }
    }
}
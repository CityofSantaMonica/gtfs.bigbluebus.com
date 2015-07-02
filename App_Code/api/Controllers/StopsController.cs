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
    public class StopsController : ApiController
    {
        [Route("api/stops")]
        public Dictionary<String, ViewModels.Stop> GetAllTrips()
        {
            return new gtfs(HttpContext.Current).stops.Values.Select(stop=>new ViewModels.Stop(stop)).ToDictionary(trip=>trip.stop_id);
        }
        [Route("api/stops/{stop_id}")]
        public IHttpActionResult GetTrip(String stop_id)
        {
            var stops = new gtfs(HttpContext.Current).stops;
            if (stops.ContainsKey(stop_id))
                return Ok(new ViewModels.Stop(stops[stop_id]));
            else
                return NotFound();
        }
    }
}
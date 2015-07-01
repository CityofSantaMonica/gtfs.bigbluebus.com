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
    public class TripsController : ApiController
    {
        public IEnumerable<ViewModels.Trip> GetAllTrips()
        {
            return new gtfs(HttpContext.Current).trips.Values.Select(trip=> new ViewModels.Trip(trip));
        }
        [Route("api/trips/{id}")]
        public IHttpActionResult GetTrip(String id)
        {
            var trips = new gtfs(HttpContext.Current).trips;
            if (trips.ContainsKey(id))
                return Ok(new ViewModels.Trip(trips[id]));
            else
                return NotFound();
        }
        [Route("api/trips/{id}/stop_times")]
        public IHttpActionResult GetTripStop_Times(String id)
        {
            var trips = new gtfs(HttpContext.Current).trips;
            if (trips.ContainsKey(id))
                return Ok(new ViewModels.TripStop_Times(trips[id]));
            else
                return NotFound();
        }
        [Route("api/trips/{id}/stop_times/stop")]
        public IHttpActionResult GetTripStop_TimesStop(String id)
        {
            var trips = new gtfs(HttpContext.Current).trips;
            if (trips.ContainsKey(id))
                return Ok(new ViewModels.TripStop_TimesStop(trips[id]));
            else
                return NotFound();
        }
    }
}
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
        [Route("api/trips")]
        public Dictionary<String, ViewModels.Trip> GetAllTrips()
        {
            return new gtfs(HttpContext.Current).trips.Values.Select(trip=>new ViewModels.Trip(trip)).ToDictionary(trip=>trip.trip_id);
        }
        [Route("api/trips/{trip_id}")]
        public IHttpActionResult GetTrip(String trip_id)
        {
            var trips = new gtfs(HttpContext.Current).trips;
            if (trips.ContainsKey(trip_id))
                return Ok(new ViewModels.Trip(trips[trip_id]));
            else
                return NotFound();
        }
        [Route("api/trips/{trip_id}/stop_times")]
        public IHttpActionResult GetTripStop_Times(String trip_id)
        {
            var trips = new gtfs(HttpContext.Current).trips;
            if (trips.ContainsKey(trip_id))
                return Ok(new ViewModels.TripStop_Times(trips[trip_id]));
            else
                return NotFound();
        }
        [Route("api/trips/{trip_id}/stop_times/stop")]
        public IHttpActionResult GetTripStop_TimesStop(String trip_id)
        {
            var trips = new gtfs(HttpContext.Current).trips;
            if (trips.ContainsKey(trip_id))
                return Ok(new ViewModels.TripStop_TimesStop(trips[trip_id]));
            else
                return NotFound();
        }
    }
}
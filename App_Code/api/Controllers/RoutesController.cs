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
    public class RoutesController : ApiController
    {
        [Route("api/routes")]
        public IEnumerable<ViewModels.Route> GetAllRoutes()
        {
            return new gtfs(HttpContext.Current).routes.Values.Select(route=>new ViewModels.Route(route));
        }

        [Route("api/routes/{route_id}")]
        public IHttpActionResult GetRoute(String route_id)
        {
            var routes = new gtfs(HttpContext.Current).routes;
            if (routes.ContainsKey(route_id))
                return Ok(new ViewModels.Route(routes[route_id]));
            else
                return NotFound();
        }

        [Route("api/routes/{route_id}/trips")]
        public IHttpActionResult GetRouteTrips(String route_id)
        {
            var routes = new gtfs(HttpContext.Current).routes;
            if (routes.ContainsKey(route_id))
                return Ok(new ViewModels.RouteTrips(routes[route_id]));
            else
                return NotFound();
        }
    }
}
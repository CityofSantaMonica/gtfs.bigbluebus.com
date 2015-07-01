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
        public IEnumerable<ViewModels.Route> GetAllRoutes()
        {
            return new gtfs(HttpContext.Current).routes.Values.Select(route=>new ViewModels.Route(route));
        }
        [Route("api/routes/{id}")]
        public IHttpActionResult GetRoute(String id)
        {
            var routes = new gtfs(HttpContext.Current).routes;
            if (routes.ContainsKey(id))
                return Ok(new ViewModels.Route(routes[id]));
            else
                return NotFound();
        }
        [Route("api/routes/{id}/trips")]
        public IHttpActionResult GetRouteTrips(String id)
        {
            var routes = new gtfs(HttpContext.Current).routes;
            if (routes.ContainsKey(id))
                return Ok(new ViewModels.RouteTrips(routes[id]));
            else
                return NotFound();
        }
    }
}
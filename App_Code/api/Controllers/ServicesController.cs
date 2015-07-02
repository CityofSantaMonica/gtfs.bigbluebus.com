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
    public class ServicesController : ApiController
    {
        private IEnumerable<Models.service> StandardServices(Models.gtfs gtfs)
        {
            return gtfs.services.Values.Where(service => (service.monday && service.tuesday && service.wednesday && service.thursday && service.friday) || service.saturday || service.sunday);
        }
        [Route("api/services")]
        public Dictionary<String, ViewModels.Service> GetAllServices()
        {
            return new gtfs(HttpContext.Current).services.Values.Select(service => new ViewModels.Service(service)).ToDictionary(service=>service.service_id);
        }
        [Route("api/services/{id}")]
        public IHttpActionResult GetService(String id)
        {
            var services = new gtfs(HttpContext.Current).services;
            if (services.ContainsKey(id))
                return Ok(new ViewModels.Service(services[id]));
            else
                return NotFound();
        }
        [Route("api/services/{service_id}/routes")]
        public IHttpActionResult GetServiceRoutes(String service_id)
        {
            var gtfs = new gtfs(HttpContext.Current);
            var services = gtfs.services;
            var routes = gtfs.routes;
            if (services.ContainsKey(service_id))
                return Ok(new ViewModels.ServiceRoutes(services[service_id]));
            else
                return NotFound();
        }
        [Route("api/services/{service_id}/routes/{route_id}/trips/stops")]
        public IHttpActionResult GetServiceRouteTripsStops(String service_id, String route_id)
        {
            var gtfs = new gtfs(HttpContext.Current);
            var services = gtfs.services;
            var routes = gtfs.routes;
            if (services.ContainsKey(service_id) && routes.ContainsKey(route_id))
                return Ok(new ViewModels.ServiceRoute(services[service_id], routes[route_id]));
            else
                return NotFound();
        }
        [Route("api/services/dateranges")]
        public IEnumerable<ViewModels.ServiceDateRange> GetService()
        {
            var services = new gtfs(HttpContext.Current).services;
            return services.Values.Select(service => new Tuple<DateTime, DateTime>(service.start_date, service.end_date)).Distinct().Select(tuple => new ViewModels.ServiceDateRange { start_date = tuple.Item1, end_date = tuple.Item2 });
        }
        [Route("api/services/{start_date:datetime}/{end_date:datetime}/standard")]
        public IHttpActionResult GetServicesDateRangeStandard(DateTime start_date, DateTime end_date)
        {
            var gtfs = new Models.gtfs(HttpContext.Current);
            var services = StandardServices(gtfs).Where(service => service.start_date.Equals(start_date) && service.end_date.Equals(end_date));
            if (services.Count() > 0)
                return Ok(services.Select(service => new ViewModels.Service(service)));
            else
                return NotFound();
        }
        [Route("api/services/standard")]
        public IEnumerable<ViewModels.ServiceStandard> GetServicesStandard()
        {
            var gtfs = new Models.gtfs(HttpContext.Current);
            var services = StandardServices(gtfs);

            return services.Select(service => new ViewModels.ServiceStandard(service));
        }
        [Route("api/services/standard/routes")]
        public IEnumerable<ViewModels.ServiceStandardRoutes> GetServicesStandardRoutes()
        {
            var gtfs = new Models.gtfs(HttpContext.Current);
            var services = StandardServices(gtfs);

            return services.Select(service => new ViewModels.ServiceStandardRoutes(service));
        }
        [Route("api/services/standard/routes/directions")]
        public IEnumerable<ViewModels.ServiceStandardRoutesDirections> GetServicesStandardRoutesDirections()
        {
            var gtfs = new Models.gtfs(HttpContext.Current);
            var services = StandardServices(gtfs);

            return services.Select(service => new ViewModels.ServiceStandardRoutesDirections(service));
        }
        [Route("api/services/standard/routes/directions/mapinfo")]
        public IEnumerable<ViewModels.ServiceStandardRoutesDirectionsMapInfo> GetServicesStandardRoutesDirectionsMapInfo()
        {
            var gtfs = new Models.gtfs(HttpContext.Current);
            var services = StandardServices(gtfs);

            return services.Select(service => new ViewModels.ServiceStandardRoutesDirectionsMapInfo(service));
        }
        [Route("api/services/standard/routes/{route_id}/directions")]
        public IHttpActionResult GetServicesStandardRoutesDirections(String route_id)
        {
            var gtfs = new Models.gtfs(HttpContext.Current);
            var routes = gtfs.routes;
            var services = StandardServices(gtfs);

            if (routes.ContainsKey(route_id))
                return Ok(services.Select(service => new ViewModels.ServiceStandardRoutesDirections(service, routes[route_id])));
            else
                return NotFound();
        }
        [Route("api/services/standard/routes/{route_id}/directions/mapinfo")]
        public IHttpActionResult GetServicesStandardRoutesDirectionsMapInfo(String route_id)
        {
            var gtfs = new Models.gtfs(HttpContext.Current);
            var routes = gtfs.routes;
            var services = StandardServices(gtfs);

            if (routes.ContainsKey(route_id))
                return Ok(services.Select(service => new ViewModels.ServiceStandardRoutesDirectionsMapInfo(service, routes[route_id])));
            else
                return NotFound();
        }
    }
}
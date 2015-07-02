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
        private Boolean DayMatchesDate(Models.service service, DateTime date)
        {
            switch (date.DayOfWeek)
            {
                case DayOfWeek.Monday:
                    return service.monday;
                case DayOfWeek.Tuesday:
                    return service.tuesday;
                case DayOfWeek.Wednesday:
                    return service.wednesday;
                case DayOfWeek.Thursday:
                    return service.thursday;
                case DayOfWeek.Friday:
                    return service.friday;
                case DayOfWeek.Saturday:
                    return service.saturday;
                case DayOfWeek.Sunday:
                    return service.sunday;
            }
            return false;
        }
        private IEnumerable<Models.service> ServicesByDate(Models.gtfs gtfs, DateTime date)
        {
            return gtfs.services.Values.Where(service => (service.start_date <= date && service.end_date >= date && DayMatchesDate(service, date) && !service.calendar_dates.Any(calendar_date => calendar_date.date == date && calendar_date.exception_type == "2")) || service.calendar_dates.Any(calendar_date => calendar_date.date == date && calendar_date.exception_type == "1"));
        }
        private IEnumerable<Models.service> StandardServices(Models.gtfs gtfs)
        {
            return gtfs.services.Values.Where(service => (service.monday && service.tuesday && service.wednesday && service.thursday && service.friday) || service.saturday || service.sunday);
        }
        [Route("api/services")]
        public Dictionary<String, ViewModels.Service> GetAllServices()
        {
            return new gtfs(HttpContext.Current).services.Values.Select(service => new ViewModels.Service(service)).ToDictionary(service => service.service_id);
        }
        [Route("api/services/calendar_dates")]
        public Dictionary<String, ViewModels.ServiceCalendar_Dates> GetServicesCalendar_Dates()
        {
            return new gtfs(HttpContext.Current).services.Values.Select(service => new ViewModels.ServiceCalendar_Dates(service)).ToDictionary(service => service.service_id);
        }
        [Route("api/services/{date:datetime}")]
        public IHttpActionResult GetServicesByDate(DateTime date)
        {
            var gtfs = new gtfs(HttpContext.Current);
            var services = ServicesByDate(gtfs, date);
            if (services.Count() > 0)
                return Ok(services.Select(service => new ViewModels.Service(service)).ToDictionary(service => service.service_id));
            else
                return NotFound();
        }
        [Route("api/services/{service_id}")]
        public IHttpActionResult GetService(String service_id)
        {
            var services = new gtfs(HttpContext.Current).services;
            if (services.ContainsKey(service_id))
                return Ok(new ViewModels.Service(services[service_id]));
            else
                return NotFound();
        }
        [Route("api/services/{date:datetime}/routes")]
        public IHttpActionResult GetServicesByDateRoutes(DateTime date)
        {
            var gtfs = new gtfs(HttpContext.Current);
            var services = ServicesByDate(gtfs, date);
            if (services.Count()>0)
                return Ok(services.Select(service => new ViewModels.ServiceRoutes(service)));
            else
                return NotFound();
        }
        [Route("api/services/{date:datetime}/routes/trips")]
        public IHttpActionResult GetServicesByDateRoutesTrips(DateTime date)
        {
            var gtfs = new gtfs(HttpContext.Current);
            var services = ServicesByDate(gtfs, date);
            if (services.Count()>0)
                return Ok(services.Select(service => new ViewModels.ServiceRoutesTrips(service)));
            else
                return NotFound();
        }
        [Route("api/services/{service_id}/routes")]
        public IHttpActionResult GetServiceRoutes(String service_id)
        {
            var gtfs = new gtfs(HttpContext.Current);
            var services = gtfs.services;
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
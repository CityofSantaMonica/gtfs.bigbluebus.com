using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Web;

namespace api.ViewModels
{
    [DataContract(Name = "service")]
    public class Service
    {
        [DataMember]
        public String service_id { get; set; }
        [DataMember]
        public Boolean monday { get; set; }
        [DataMember]
        public Boolean tuesday { get; set; }
        [DataMember]
        public Boolean wednesday { get; set; }
        [DataMember]
        public Boolean thursday { get; set; }
        [DataMember]
        public Boolean friday { get; set; }
        [DataMember]
        public Boolean saturday { get; set; }
        [DataMember]
        public Boolean sunday { get; set; }
        [DataMember]
        public DateTime start_date { get; set; }
        [DataMember]
        public DateTime end_date { get; set; }

        public Service() { }
        public Service(Models.service service)
        {
            this.service_id = service.service_id;
            this.monday = service.monday;
            this.tuesday = service.tuesday;
            this.wednesday = service.wednesday;
            this.thursday = service.thursday;
            this.friday = service.friday;
            this.saturday = service.saturday;
            this.sunday = service.sunday;
            this.start_date = service.start_date;
            this.end_date = service.end_date;
        }
    }
    [DataContract(Name = "service")]
    public class ServiceCalendar_Dates : Service
    {
        [DataMember]
        public IEnumerable<Calendar_Date> calendar_dates { get; set; }

        public ServiceCalendar_Dates() { }
        public ServiceCalendar_Dates(Models.service service)
            : base(service)
        {
            this.calendar_dates = service.calendar_dates.Select(calendar_date => new Calendar_Date(calendar_date));
        }
    }
    [DataContract(Name = "service")]
    public class ServiceRoute : Service
    {
        [DataMember]
        public RouteTrips route { get; set; }

        public ServiceRoute() { }
        public ServiceRoute(Models.service service, Models.route route)
            : base(service)
        {
            this.route = new RouteTrips(route);
        }
    }
    [DataContract(Name = "service")]
    public class ServiceRoutes : Service
    {
        [DataMember]
        public IEnumerable<Route> routes { get; set; }

        public ServiceRoutes() { }
        public ServiceRoutes(Models.service service)
            : base(service)
        {
            this.routes = service.trips.Values.Select(trip => trip.route).Distinct().Select(route => new Route(route));
        }
    }
    [DataContract(Name = "service")]
    public class ServiceRoutesTrips : Service
    {
        [DataMember]
        public IEnumerable<RouteTrips> routes { get; set; }

        public ServiceRoutesTrips() { }
        public ServiceRoutesTrips(Models.service service)
            : base(service)
        {
            this.routes = service.trips.Values.Select(trip => trip.route).Distinct().Select(route => new RouteTrips(route, service));
        }
    }
    [DataContract(Name = "service")]
    public class ServiceDateRange
    {
        [DataMember]
        public DateTime start_date { get; set; }
        [DataMember]
        public DateTime end_date { get; set; }

        public ServiceDateRange() { }
        public ServiceDateRange(Models.service service)
        {
            this.start_date = service.start_date;
            this.end_date = service.end_date;
        }
    }
    [DataContract(Name = "service")]
    public class ServiceStandard : ServiceDateRange
    {
        [DataMember]
        public String service_id { get; set; }
        [DataMember]
        public String name { get; set; }

        public ServiceStandard() { }
        public ServiceStandard(Models.service service)
            : base(service)
        {
            this.service_id = service.service_id;
            if (service.monday && service.tuesday && service.wednesday && service.thursday && service.friday && !service.saturday && !service.sunday)
                this.name = "Weekday";
            if (!service.monday && !service.tuesday && !service.wednesday && !service.thursday && !service.friday && service.saturday && service.sunday)
                this.name = "Weekend";
            if (!service.monday && !service.tuesday && !service.wednesday && !service.thursday && !service.friday && service.saturday && !service.sunday)
                this.name = "Saturday";
            if (!service.monday && !service.tuesday && !service.wednesday && !service.thursday && !service.friday && !service.saturday && service.sunday)
                this.name = "Sunday";
        }
    }
    [DataContract(Name = "service")]
    public class ServiceStandardRoutes : ServiceStandard
    {
        [DataMember]
        public IEnumerable<Route> routes { get; set; }

        public ServiceStandardRoutes() { }
        public ServiceStandardRoutes(Models.service service)
            : base(service)
        {
            this.routes = service.trips.Values.Select(trip => trip.route).Distinct().Select(route => new Route(route));
        }
    }
    [DataContract(Name = "service")]
    public class ServiceStandardRoutesDirections : ServiceStandard
    {
        [DataMember]
        public IEnumerable<RouteDirections> routeDirections { get; set; }

        public ServiceStandardRoutesDirections() { }
        public ServiceStandardRoutesDirections(Models.service service)
            : base(service)
        {
            this.routeDirections = service.trips.Values.GroupBy(trip => trip.route).Select(group => new RouteDirections(group.Key, service));
        }
        public ServiceStandardRoutesDirections(Models.service service, Models.route route)
            : base(service)
        {
            this.routeDirections = service.trips.Values.Where(trip => trip.route == route).GroupBy(trip => trip.route).Select(group => new RouteDirections(group.Key, service));
        }
    }
    [DataContract(Name = "service")]
    public class ServiceStandardRoutesDirectionsMapInfo : ServiceStandard
    {
        [DataMember]
        public IEnumerable<RouteDirectionsMapInfo> routes { get; set; }

        public ServiceStandardRoutesDirectionsMapInfo() { }
        public ServiceStandardRoutesDirectionsMapInfo(Models.service service)
            : base(service)
        {
            this.routes = service.trips.Values.GroupBy(trip => trip.route).Select(group => new RouteDirectionsMapInfo(group.Key, service));
        }
        public ServiceStandardRoutesDirectionsMapInfo(Models.service service, Models.route route)
            : base(service)
        {
            this.routes = service.trips.Values.Where(trip => trip.route == route).GroupBy(trip => trip.route).Select(group => new RouteDirectionsMapInfo(group.Key, service));
        }
    }
}
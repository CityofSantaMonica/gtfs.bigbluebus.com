using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Web;

namespace api.ViewModels
{
    [DataContract(Name="route")]
    public class Route
    {
        [DataMember]
        public String route_id { get; set; }
        [DataMember]
        public String agency_id { get; set; }
        [DataMember]
        public String route_short_name { get; set; }
        [DataMember]
        public String route_long_name { get; set; }
        [DataMember]
        public String route_desc { get; set; }
        [DataMember]
        public String route_type { get; set; }
        [DataMember]
        public String route_url { get; set; }
        [DataMember]
        public String route_color { get; set; }
        [DataMember]
        public String route_text_color { get; set; }
        public Route(Models.route route)
        {
            this.agency_id = route.agency_id;
            this.route_color = route.route_color;
            this.route_desc = route.route_desc;
            this.route_id = route.route_id;
            this.route_long_name = route.route_long_name;
            this.route_short_name = route.route_short_name;
            this.route_text_color = route.route_text_color;
            this.route_type = route.route_type;
            this.route_url = route.route_url;
        }
    }
    [DataContract(Name="route")]
    public class RouteTrips : Route
    {
        [DataMember]
        public IEnumerable<Trip> trips { get; set; }
        public RouteTrips(Models.route route)
            : base(route)
        {
            this.trips = route.trips.Values.Select(trip => new Trip(trip));
        }
        public RouteTrips(Models.route route, Models.service service)
            : base(route)
        {
            this.trips = route.trips.Values.Where(trip => trip.service_id == service.service_id).Select(trip => new Trip(trip));
        }
    }
    [DataContract(Name="route")]
    public class RouteDirections : Route
    {
        [DataMember]
        public IEnumerable<Direction> directions { get; set; }
        public RouteDirections(Models.route route)
            : base(route)
        {
            this.directions = route.directions.Values.Select(direction => new Direction(direction));
        }
        public RouteDirections(Models.route route, Models.service service)
            : base(route)
        {
            this.directions = route.directions.Values.GroupJoin(service.trips.Values, outer => outer, inner => inner.direction, (outer, inner) => new Direction(outer));
        }
    }
    [DataContract(Name="route")]
    public class RouteDirectionsMapInfo : Route
    {
        [DataMember]
        public IEnumerable<DirectionMapInfo> directions { get; set; }
        public RouteDirectionsMapInfo(Models.route route)
            : base(route)
        {
            this.directions = route.directions.Values.Select(direction => new DirectionMapInfo(direction));
        }
        public RouteDirectionsMapInfo(Models.route route, Models.service service)
            : base(route)
        {
            this.directions = route.directions.Values.Select(direction => new DirectionMapInfo(direction, service));
        }
    }
    [DataContract(Name="route")]
    public class RouteDirectionsTrips : Route
    {
        [DataMember]
        public IEnumerable<DirectionTrips> directions { get; set; }
        public RouteDirectionsTrips(Models.route route)
            : base(route)
        {
            this.directions = route.directions.Values.Select(direction => new DirectionTrips(direction));
        }
        public RouteDirectionsTrips(Models.route route, Models.service service)
            : base(route)
        {
            this.directions = route.directions.Values.Select(direction => new DirectionTrips(direction, service));
        }
    }
    [DataContract(Name="route")]
    public class RouteTripsStop_Times : Route
    {
        [DataMember]
        public IEnumerable<TripStop_Times> trips { get; set; }
        public RouteTripsStop_Times(Models.route route)
            : base(route)
        {
            this.trips = route.trips.Values.Select(trip => new TripStop_Times(trip));
        }
        public RouteTripsStop_Times(Models.route route, Models.service service)
            : base(route)
        {
            this.trips = route.trips.Values.Where(trip => trip.service_id == service.service_id).Select(trip => new TripStop_Times(trip));
        }
    }
}
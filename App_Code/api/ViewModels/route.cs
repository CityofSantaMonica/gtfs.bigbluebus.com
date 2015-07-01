using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Web;

namespace api.ViewModels
{
    [DataContract]
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
        public Route(api.Models.route route){
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
    [DataContract]
    public class RouteTrips:Route
    {
        [DataMember]
        public IEnumerable<Trip> trips { get; set; }
        public RouteTrips(api.Models.route route):base(route)
        {
            this.trips = route.trips.Values.Select(trip => new Trip(trip));
        }
        public RouteTrips(api.Models.route route, api.Models.service service):base(route){
            this.trips = route.trips.Values.Where(trip=>trip.service_id == service.service_id).Select(trip=> new Trip(trip));
        }
    }
    [DataContract]
    public class RouteTripsStop_Times:Route
    {
        [DataMember]
        public IEnumerable<TripStop_Times> trips { get; set; }
        public RouteTripsStop_Times(api.Models.route route):base(route)
        {
            this.trips = route.trips.Values.Select(trip => new TripStop_Times(trip));
        }
        public RouteTripsStop_Times(api.Models.route route, api.Models.service service)
            : base(route)
        {
            this.trips = route.trips.Values.Where(trip => trip.service_id == service.service_id).Select(trip => new TripStop_Times(trip));
        }
    }
}
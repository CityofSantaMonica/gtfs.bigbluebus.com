using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Web;

namespace api.Models
{
    [DataContract]
    public class trip
    {
        [DataMember]
        public String route_id { get; set; }
        [DataMember]
        public String service_id { get; set; }
        [DataMember]
        public String trip_id { get; set; }
        [DataMember]
        public String trip_headsign { get; set; }
        [DataMember]
        public String trip_short_name { get; set; }
        [DataMember]
        public String direction_id { get; set; }
        [DataMember]
        public String block_id { get; set; }
        [DataMember]
        public String shape_id { get; set; }
        [DataMember]
        public String wheelchair_accessible { get; set; }
        [DataMember]
        public String bikes_allowed { get; set; }

        public route route { get; set; }
        public service service { get; set; }
        public stop_times_sequence stop_times_sequence { get; set; }
    }
    public class trips : Dictionary<String, trip>
    {
        public void Join(routes routes)
        {
            this.Values.ToList().ForEach(trip => {
                trip.route = routes[trip.route_id];
                trip.route.trips.Add(trip.trip_id, trip); 
            });
        }
        public void Join(services services)
        {
            this.Values.ToList().ForEach(trip => { 
                trip.service = services[trip.service_id]; 
                trip.service.trips.Add(trip.trip_id, trip); 
            });
        }
        public void Join(stop_times_trips stop_times_trips)
        {
            this.Values.ToList().ForEach(trip => {
                trip.stop_times_sequence = stop_times_trips[trip.trip_id]; 
            });
        }
    }
}
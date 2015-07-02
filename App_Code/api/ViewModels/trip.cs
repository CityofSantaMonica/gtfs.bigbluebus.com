using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Web;

namespace api.ViewModels
{
    [DataContract(Name="trip")]
    public class Trip
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
        public Trip(api.Models.trip trip)
        {
            this.route_id = trip.route_id;
            this.service_id = trip.service_id;
            this.trip_id = trip.trip_id;
            this.trip_headsign = trip.trip_headsign;
            this.trip_short_name = trip.trip_short_name;
            this.direction_id = trip.direction_id;
            this.block_id = trip.block_id;
            this.shape_id = trip.shape_id;
            this.wheelchair_accessible = trip.wheelchair_accessible;
            this.bikes_allowed = trip.bikes_allowed;
        }
    }
    [DataContract(Name="trip")]
    public class TripStop_Times:Trip
    {
        [DataMember]
        public IEnumerable<Stop_Time> stop_times { get; set; }

        public TripStop_Times(api.Models.trip trip):base(trip)
        {
            this.stop_times = trip.stop_times_sequence.Values.Select(stop_time => new Stop_Time(stop_time));
        }
    }
    [DataContract(Name="trip")]
    public class TripStop_TimesStop:Trip
    {
        [DataMember]
        public IEnumerable<Stop_TimeStop> stop_times { get; set; }

        public TripStop_TimesStop(api.Models.trip trip):base(trip)
        {
            this.stop_times = trip.stop_times_sequence.Values.Select(stop_time => new Stop_TimeStop(stop_time));
        }
    }
}
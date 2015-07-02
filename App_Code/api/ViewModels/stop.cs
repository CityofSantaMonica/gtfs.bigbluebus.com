using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Web;

namespace api.ViewModels
{
    [DataContract(Name="stop")]
    public class Stop
    {
        [DataMember]
        public String stop_id { get; set; }
        [DataMember]
        public String stop_code { get; set; }
        [DataMember]
        public String stop_name { get; set; }
        [DataMember]
        public String stop_desc { get; set; }
        [DataMember]
        public Decimal stop_lat { get; set; }
        [DataMember]
        public Decimal stop_lon { get; set; }
        [DataMember]
        public String zone_id { get; set; }
        [DataMember]
        public String stop_url { get; set; }
        [DataMember]
        public String location_type { get; set; }
        [DataMember]
        public String parent_station { get; set; }
        [DataMember]
        public String stop_timezone { get; set; }
        [DataMember]
        public String wheelchair_boarding { get; set; }

        public Stop(Models.stop stop)
        {
            this.stop_id = stop.stop_id;
            this.stop_code = stop.stop_code;
            this.stop_name = stop.stop_name;
            this.stop_desc = stop.stop_desc;
            this.stop_lat = stop.stop_lat;
            this.stop_lon = stop.stop_lon;
            this.zone_id = stop.zone_id;
            this.stop_url = stop.stop_url;
            this.location_type = stop.location_type;
            this.parent_station = stop.parent_station;
            this.stop_timezone = stop.stop_timezone;
            this.wheelchair_boarding = stop.wheelchair_boarding;
        }
    }
    [DataContract(Name="stop")]
    public class StopStop_Times : Stop
    {
        [DataMember]
        public IEnumerable<Stop_Time> stop_times { get; set; }

        public StopStop_Times(Models.stop stop, Models.direction direction)
            : base(stop)
        {
            this.stop_times = direction.trips.Values.SelectMany(trip => trip.stop_times_sequence.Values.Where(stop_time => stop_time.stop == stop && stop_time.arrival_time.HasValue).Select(stop_time => new Stop_Time(stop_time))).OrderBy(stop_time => stop_time.arrival_time);
        }
        public StopStop_Times(Models.stop stop, Models.direction direction, Models.service service)
            : base(stop)
        {
            this.stop_times = direction.trips.Values.Where(trip=>trip.service==service).SelectMany(trip => trip.stop_times_sequence.Values.Where(stop_time => stop_time.stop == stop && stop_time.arrival_time.HasValue).Select(stop_time => new Stop_Time(stop_time))).OrderBy(stop_time => stop_time.arrival_time);
        }
    }
}
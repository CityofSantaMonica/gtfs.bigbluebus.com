using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Web;

namespace gtfs_json
{
    [DataContract]
    public class stop_time
    {
        private DateTime? ParseTime(String time_string)
        {
            if (!String.IsNullOrEmpty(time_string))
            {
                var time_parts = this.arrival_time_string.Split(':');
                return new DateTime().Add(new TimeSpan(Int32.Parse(time_parts[0]), Int32.Parse(time_parts[1]), Int32.Parse(time_parts[2])));
            }
            else
                return null;
        }
        [DataMember]
        public String trip_id { get; set; }
        [DataMember(Name = "arrival_time")]
        public String arrival_time_string { get; set; }
        public DateTime? arrival_time { get; set; }
        [DataMember(Name = "departure_time")]
        public String departure_time_string { get; set; }
        public DateTime? departure_time { get; set; }
        [DataMember]
        public String stop_id { get; set; }
        [DataMember(Name = "stop_sequence")]
        public String stop_sequence_string { get; set; }
        public UInt32 stop_sequence { get; set; }
        [DataMember]
        public String stop_headsign { get; set; }
        [DataMember]
        public String pickup_type { get; set; }
        [DataMember]
        public String drop_off_type { get; set; }
        [DataMember(Name = "shape_dist_traveled")]
        public String shape_dist_traveled_string { get; set; }
        public Decimal shape_dist_traveled { get; set; }
        [DataMember]
        public String timepoint { get; set; }
        [OnDeserialized]
        internal void OnDeserializedMethod(StreamingContext context)
        {
            this.arrival_time = ParseTime(this.arrival_time_string);
            this.departure_time = ParseTime(this.departure_time_string);
            this.stop_sequence = UInt32.Parse(this.stop_sequence_string);
            var testDecimal = new Decimal();
            if (Decimal.TryParse(this.shape_dist_traveled_string, out testDecimal))
                this.shape_dist_traveled = testDecimal;
        }
        public stop stop { get; set; }
        public stop_time()
        {
        }
    }
    public class stop_times_sequence : Dictionary<UInt32, stop_time>
    {

    }
    public class stop_times_trips : Dictionary<String, stop_times_sequence>
    {
        public void Join(stops stops)
        {
            this.Values.ToList().ForEach(trip => trip.Values.ToList().ForEach(stop_time => stop_time.stop = stops[stop_time.stop_id]));
        }
    }
}
using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Web;

namespace api.ViewModels
{
    [DataContract(Name="stop_time")]
    public class Stop_Time
    {
        [DataMember]
        public String trip_id { get; set; }
        [DataMember]
        public DateTime? arrival_time { get; set; }
        [DataMember]
        public DateTime? departure_time { get; set; }
        [DataMember]
        public String stop_id { get; set; }
        [DataMember]
        public UInt32 stop_sequence { get; set; }
        [DataMember]
        public String stop_headsign { get; set; }
        [DataMember]
        public String pickup_type { get; set; }
        [DataMember]
        public String drop_off_type { get; set; }
        [DataMember]
        public Decimal shape_dist_traveled { get; set; }
        [DataMember]
        public String timepoint { get; set; }
        public Stop_Time(api.Models.stop_time stop_time)
        {
            this.trip_id = stop_time.trip_id;
            this.arrival_time = stop_time.arrival_time;
            this.departure_time = stop_time.departure_time;
            this.stop_id = stop_time.stop_id;
            this.stop_sequence = stop_time.stop_sequence;
            this.stop_headsign = stop_time.stop_headsign;
            this.pickup_type = stop_time.pickup_type;
            this.drop_off_type = stop_time.drop_off_type;
            this.shape_dist_traveled = stop_time.shape_dist_traveled;
            this.timepoint = stop_time.timepoint;
        }
    }
    [DataContract(Name="stop_time")]
    public class Stop_TimeStop:Stop_Time
    {
        [DataMember]
        public Stop Stop { get; set; }
        public Stop_TimeStop(api.Models.stop_time stop_time):base(stop_time)
        {
            this.Stop = new Stop(stop_time.stop);
        }
    }
}
using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Web;

namespace api.Models
{
    [DataContract]
    public class stop
    {
        [DataMember]
        public String stop_id { get; set; }
        [DataMember]
        public String stop_code { get; set; }
        [DataMember]
        public String stop_name { get; set; }
        [DataMember]
        public String stop_desc { get; set; }
        [DataMember(Name = "stop_lat")]
        public String stop_lat_string { get; set; }
        public Decimal stop_lat { get; set; }
        [DataMember(Name = "stop_lon")]
        public String stop_lon_string { get; set; }
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
        [OnDeserialized]
        internal void OnDeserializedMethod(StreamingContext context)
        {
            var test = new Decimal();
            if (Decimal.TryParse(this.stop_lat_string, out test))
                this.stop_lat = test;
            if (Decimal.TryParse(this.stop_lon_string, out test))
                this.stop_lon = test;
        }

        public stop()
        {
        }
    }
    public class stops : Dictionary<String, stop>
    {

    }
}
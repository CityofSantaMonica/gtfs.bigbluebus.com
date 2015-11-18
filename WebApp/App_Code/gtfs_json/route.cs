using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Web;

namespace gtfs_json
{
    [DataContract]
    public class route
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

        public route()
        {
            trips = new trips();
            directions = new directions();
        }
        public trips trips { get; set; }
        public directions directions { get; set; }
    }
    public class routes : Dictionary<String, route>
    {
    }
}
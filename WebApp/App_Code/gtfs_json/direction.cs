using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Web;

namespace gtfs_json
{
    [DataContract]
    public class direction
    {
        [DataMember]
        public String direction_id { get; set; }
        public direction(String direction_id)
        {
            this.direction_id = direction_id;
            trips = new trips();
        }
        public trips trips { get; set; }
    }
    public class directions : Dictionary<String, direction>
    {

    }
}
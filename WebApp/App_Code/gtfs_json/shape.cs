using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Text;
using System.Threading.Tasks;

namespace gtfs_json
{
    [DataContract]
    public class shape_pt
    {
        [DataMember(Name = "shape_pt_lat")]
        public String shape_pt_lat_string { get; set; }
        public Decimal shape_pt_lat { get; set; }
        [DataMember(Name = "shape_pt_lon")]
        public String shape_pt_lon_string { get; set; }
        public Decimal shape_pt_lon { get; set; }
        [OnDeserialized]
        internal void OnDeserializedMethod(StreamingContext context)
        {
            var test = new Decimal();
            if (Decimal.TryParse(this.shape_pt_lat_string, out test))
                this.shape_pt_lat = test;
            if (Decimal.TryParse(this.shape_pt_lon_string, out test))
                this.shape_pt_lon = test;
        }
    }
    [DataContract]
    public class shape
    {
        [DataMember]
        public String shape_id { get; set; }
        [DataMember]
        public IEnumerable<shape_pt> points { get; set; }
    }
    public class shapes : Dictionary<String, shape>
    {

    }
}

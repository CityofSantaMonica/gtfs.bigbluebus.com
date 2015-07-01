using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Web;

namespace api.ViewModels
{
    [DataContract]
    public class Shape
    {
        [DataMember]
        public String shape_id { get; set; }
    }
}
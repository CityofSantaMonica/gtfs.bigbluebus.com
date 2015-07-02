using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Web;

namespace api.ViewModels
{
    [DataContract(Name="calendar_date")]
    public class Calendar_Date
    {
        [DataMember]
        public String service_id { get; set; }
        [DataMember]
        public DateTime date { get; set; }
        [DataMember]
        public String exception_type { get; set; }

        public Calendar_Date(Models.calendar_date calendar_date)
        {
            this.service_id = calendar_date.service_id;
            this.date = calendar_date.date;
            this.exception_type = calendar_date.exception_type;
        }
    }
}
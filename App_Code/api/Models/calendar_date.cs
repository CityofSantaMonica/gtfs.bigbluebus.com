using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Web;

namespace api.Models
{
    [DataContract]
    public class calendar_date
    {
        [DataMember]
        public String service_id { get; set; }
        [DataMember(Name="date")]
        public String date_string { get; set; }
        public DateTime date { get; set; }
        [DataMember]
        public String exception_type { get; set; }
        [OnDeserialized]
        internal void OnDeserializedMethod(StreamingContext context)
        {
            var test = new DateTime();
            if (DateTime.TryParseExact(this.date_string, "yyyyMMdd", System.Globalization.CultureInfo.CurrentCulture, System.Globalization.DateTimeStyles.None, out test))
                this.date = test;
        }

        public calendar_date()
        {
        }
        public service service { get; set; }
    }
    public class calendar_dates : List<calendar_date>
    {
        public void Join(services services)
        {
            this.ForEach(calendar_date =>
            {
                calendar_date.service = services[calendar_date.service_id];
                calendar_date.service.calendar_dates.Add(calendar_date);
            });
        }
    }
}
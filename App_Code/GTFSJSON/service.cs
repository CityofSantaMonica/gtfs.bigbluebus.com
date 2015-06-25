using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Web;

namespace GTFSJSON
{
    /// <summary>
    /// Summary description for service
    /// </summary>
    [DataContract]
    public class service
    {
        [DataMember]
        public String service_id { get; set; }
        [DataMember(Name="monday")]
        public String monday_string { get; set; }
        public Boolean monday { get; set; }
        [DataMember(Name = "tuesday")]
        public String tuesday_string { get; set; }
        public Boolean tuesday { get; set; }
        [DataMember(Name = "wednesday")]
        public String wednesday_string { get; set; }
        public Boolean wednesday { get; set; }
        [DataMember(Name = "thursday")]
        public String thursday_string { get; set; }
        public Boolean thursday { get; set; }
        [DataMember(Name = "friday")]
        public String friday_string { get; set; }
        public Boolean friday { get; set; }
        [DataMember(Name = "saturday")]
        public String saturday_string { get; set; }
        public Boolean saturday { get; set; }
        [DataMember(Name = "sunday")]
        public String sunday_string { get; set; }
        public Boolean sunday { get; set; }
        [DataMember(Name = "start_date")]
        public String start_date_string { get; set; }
        public DateTime start_date { get; set; }
        [DataMember(Name = "end_date")]
        public String end_date_string { get; set; }
        public DateTime end_date { get; set; }
        [OnDeserialized]
        internal void OnDeserializedMethod(StreamingContext context)
        {
            DateTime test = new DateTime();
            monday = this.monday_string == "1";
            tuesday = this.tuesday_string == "1";
            wednesday = this.wednesday_string == "1";
            thursday = this.thursday_string == "1";
            friday = this.friday_string == "1";
            saturday = this.saturday_string == "1";
            sunday = this.sunday_string == "1";
            if (DateTime.TryParseExact(this.start_date_string, "yyyyMMdd", System.Globalization.CultureInfo.CurrentCulture, System.Globalization.DateTimeStyles.None, out test))
                this.start_date = test;
            if (DateTime.TryParseExact(this.end_date_string, "yyyyMMdd", System.Globalization.CultureInfo.CurrentCulture, System.Globalization.DateTimeStyles.None, out test))
                this.end_date = test;
        }
    }
    public class services : Dictionary<String, service>
    {

    }
}
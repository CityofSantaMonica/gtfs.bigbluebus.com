using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Web;

namespace api.ViewModels
{
    [DataContract]
    public class Service
    {
        [DataMember]
        public String service_id { get; set; }
        [DataMember]
        public Boolean monday { get; set; }
        [DataMember]
        public Boolean tuesday { get; set; }
        [DataMember]
        public Boolean wednesday { get; set; }
        [DataMember]
        public Boolean thursday { get; set; }
        [DataMember]
        public Boolean friday { get; set; }
        [DataMember]
        public Boolean saturday { get; set; }
        [DataMember]
        public Boolean sunday { get; set; }
        [DataMember]
        public DateTime start_date { get; set; }
        [DataMember]
        public DateTime end_date { get; set; }

        public Service() { }
        public Service(api.Models.service service)
        {
            this.service_id = service.service_id;
            this.monday = service.monday;
            this.tuesday = service.tuesday;
            this.wednesday = service.wednesday;
            this.thursday = service.thursday;
            this.friday = service.friday;
            this.saturday = service.saturday;
            this.sunday = service.sunday;
            this.start_date = service.start_date;
            this.end_date = service.end_date;
        }
    }
    [DataContract]
    public class ServiceRoute
    {
        [DataMember]
        public String service_id { get; set; }
        [DataMember]
        public Boolean monday { get; set; }
        [DataMember]
        public Boolean tuesday { get; set; }
        [DataMember]
        public Boolean wednesday { get; set; }
        [DataMember]
        public Boolean thursday { get; set; }
        [DataMember]
        public Boolean friday { get; set; }
        [DataMember]
        public Boolean saturday { get; set; }
        [DataMember]
        public Boolean sunday { get; set; }
        [DataMember]
        public DateTime start_date { get; set; }
        [DataMember]
        public DateTime end_date { get; set; }

        public ServiceRoute() { }
        public ServiceRoute(api.Models.service service)
        {
            this.service_id = service.service_id;
            this.monday = service.monday;
            this.tuesday = service.tuesday;
            this.wednesday = service.wednesday;
            this.thursday = service.thursday;
            this.friday = service.friday;
            this.saturday = service.saturday;
            this.sunday = service.sunday;
            this.start_date = service.start_date;
            this.end_date = service.end_date;
        }
    }
    [DataContract]
    public class ServiceDateRange
    {
        [DataMember]
        public DateTime start_date { get; set; }
        [DataMember]
        public DateTime end_date { get; set; }

        public ServiceDateRange() { }
    }
}
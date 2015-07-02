using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Web;

namespace api.ViewModels
{
    [DataContract(Name="map_info")]
    public class Map_Info
    {
        [DataMember]
        public IEnumerable<Shape> shapes { get; set; }
        [DataMember]
        public IEnumerable<StopStop_Times> stops { get; set; }
        public Map_Info() { }
        public Map_Info(Models.direction direction) 
        {
            this.shapes = direction.trips.Values.Select(trip => trip.shape_id).Distinct().Select(shape_id => new Shape { shape_id = shape_id });
            this.stops = direction.trips.Values.SelectMany(trip => trip.stops.Values).Distinct().Select(stop=> new StopStop_Times(stop, direction));
        }
        public Map_Info(Models.direction direction, Models.service service) 
        {
            this.shapes = direction.trips.Values.Select(trip => trip.shape_id).Distinct().Select(shape_id => new Shape { shape_id = shape_id });
            this.stops = direction.trips.Values.Where(trip=>trip.service == service).SelectMany(trip => trip.stops.Values).Distinct().Select(stop=> new StopStop_Times(stop, direction, service));
        }
    }
}
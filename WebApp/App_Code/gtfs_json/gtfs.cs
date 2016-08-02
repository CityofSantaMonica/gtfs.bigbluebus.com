using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Web;
using System.Web.Caching;

using Newtonsoft.Json;

namespace gtfs_json
{
    public class gtfs
    {
        private stop_times_trips stop_times_trips { get; set; }
        public gtfs()
        {
            var context = HttpContext.Current;
            var serializer = new Newtonsoft.Json.JsonSerializer();
            calendar_dates = context.Cache["GTFSJSON.calendar_dates"] as calendar_dates;
            routes = context.Cache["GTFSJSON.routes"] as routes;
            services = context.Cache["GTFSJSON.services"] as services;
            //shapes = context.Cache["GTFSJSON.shapes"] as shapes;
            stops = context.Cache["GTFSJSON.stops"] as stops;
            stop_times_trips = context.Cache["GTFSJSON.stop_times_trips"] as stop_times_trips;
            trips = context.Cache["GTFSJSON.trips"] as trips;

            if (calendar_dates == null || calendar_dates.Count == 0 || routes == null || routes.Count == 0 || services == null || services.Count == 0 /* || shapes == null*/ || stops == null || stops.Count == 0 || stop_times_trips == null || stop_times_trips.Count == 0 || trips == null || trips.Count == 0)
            {
                var calendar_dates_path = context.Server.MapPath("/parsed/calendar_dates.json");
                var routes_path = context.Server.MapPath("/parsed/routes.json");
                var services_path = context.Server.MapPath("/parsed/calendar.json");
                //var shapes_path = context.Server.MapPath("/parsed/shapes.json");
                var stops_path = context.Server.MapPath("/parsed/stops.json");
                var stop_times_trips_path = context.Server.MapPath("/parsed/stop_times.json");
                var trips_path = context.Server.MapPath("/parsed/trips.json");
                using (var stream = File.Open(calendar_dates_path, FileMode.Open, FileAccess.Read, FileShare.ReadWrite))
                {
                    calendar_dates = serializer.Deserialize<calendar_dates>(new JsonTextReader(new StreamReader(stream)));
                }
                using (var stream = File.Open(routes_path, FileMode.Open, FileAccess.Read, FileShare.ReadWrite))
                {
                    routes = serializer.Deserialize<routes>(new JsonTextReader(new StreamReader(stream)));
                }
                using (var stream = File.Open(services_path, FileMode.Open, FileAccess.Read, FileShare.ReadWrite))
                {
                    services = serializer.Deserialize<services>(new JsonTextReader(new StreamReader(stream)));
                }
                //using (var stream = File.Open(shapes_path, FileMode.Open, FileAccess.Read, FileShare.ReadWrite))
                //{
                //    shapes = serializer.Deserialize<shapes>(new JsonTextReader(new StreamReader(stream)));
                //}
                using (var stream = File.Open(stops_path, FileMode.Open, FileAccess.Read, FileShare.ReadWrite))
                {
                    stops = serializer.Deserialize<stops>(new JsonTextReader(new StreamReader(stream)));
                }
                using (var stream = File.Open(stop_times_trips_path, FileMode.Open, FileAccess.Read, FileShare.ReadWrite))
                {
                    stop_times_trips = serializer.Deserialize<stop_times_trips>(new JsonTextReader(new StreamReader(stream)));
                }
                using (var stream = File.Open(trips_path, FileMode.Open, FileAccess.Read, FileShare.ReadWrite))
                {
                    trips = serializer.Deserialize<trips>(new JsonTextReader(new StreamReader(stream)));
                }
                calendar_dates.Join(services);
                stop_times_trips.Join(stops);
                trips.Join(routes);
                trips.Join(services);
                trips.Join(stop_times_trips);

                context.Cache.Add("GTFSJSON.calendar_dates", calendar_dates, new CacheDependency(calendar_dates_path), Cache.NoAbsoluteExpiration, Cache.NoSlidingExpiration, CacheItemPriority.Normal, null);
                context.Cache.Add("GTFSJSON.routes", routes, new CacheDependency(routes_path), Cache.NoAbsoluteExpiration, Cache.NoSlidingExpiration, CacheItemPriority.Normal, null);
                context.Cache.Add("GTFSJSON.services", services, new CacheDependency(services_path), Cache.NoAbsoluteExpiration, Cache.NoSlidingExpiration, CacheItemPriority.Normal, null);
                //context.Cache.Add("GTFSJSON.shapes", stops, new CacheDependency(shapes_path), Cache.NoAbsoluteExpiration, Cache.NoSlidingExpiration, CacheItemPriority.Normal, null);
                context.Cache.Add("GTFSJSON.stops", stops, new CacheDependency(stops_path), Cache.NoAbsoluteExpiration, Cache.NoSlidingExpiration, CacheItemPriority.Normal, null);
                context.Cache.Add("GTFSJSON.stop_times_trips", stop_times_trips, new CacheDependency(stop_times_trips_path), Cache.NoAbsoluteExpiration, Cache.NoSlidingExpiration, CacheItemPriority.Normal, null);
                context.Cache.Add("GTFSJSON.trips", trips, new CacheDependency(trips_path), Cache.NoAbsoluteExpiration, Cache.NoSlidingExpiration, CacheItemPriority.Normal, null);
            }
        }
        public calendar_dates calendar_dates { get; set; }
        public routes routes { get; set; }
        public services services { get; set; }
        //public shapes shapes { get; set; }
        public stops stops { get; set; }
        public trips trips { get; set; }
    }
}
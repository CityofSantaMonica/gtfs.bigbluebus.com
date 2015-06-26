using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Web;
using System.Web.Caching;

using Newtonsoft.Json;

namespace GTFSJSON
{
    public class gtfs
    {
        public gtfs(HttpContext context)
        {
            var serializer = new Newtonsoft.Json.JsonSerializer();
            routes = context.Cache["GTFSJSON.routes"] as GTFSJSON.routes;
            services = context.Cache["GTFSJSON.services"] as GTFSJSON.services;
            stops = context.Cache["GTFSJSON.stops"] as GTFSJSON.stops;
            stop_times_trips = context.Cache["GTFSJSON.stop_times_trips"] as GTFSJSON.stop_times_trips;
            trips = context.Cache["GTFSJSON.trips"] as GTFSJSON.trips;

            if (routes == null || services == null || stops == null || stop_times_trips == null || trips == null)
            {
                var routes_path = context.Server.MapPath("parsed/routes.json");
                var services_path = context.Server.MapPath("parsed/calendar.json");
                var stops_path = context.Server.MapPath("parsed/stops.json");
                var stop_times_trips_path = context.Server.MapPath("parsed/stop_times.json");
                var trips_path = context.Server.MapPath("parsed/trips.json");
                routes = serializer.Deserialize<GTFSJSON.routes>(new JsonTextReader(new StreamReader(routes_path)));
                services = serializer.Deserialize<GTFSJSON.services>(new JsonTextReader(new StreamReader(services_path)));
                stops = serializer.Deserialize<GTFSJSON.stops>(new JsonTextReader(new StreamReader(stops_path)));
                stop_times_trips = serializer.Deserialize<GTFSJSON.stop_times_trips>(new JsonTextReader(new StreamReader(stop_times_trips_path)));
                trips = serializer.Deserialize<GTFSJSON.trips>(new JsonTextReader(new StreamReader(trips_path)));

                stop_times_trips.Join(stops);
                trips.Join(routes);
                trips.Join(services);
                trips.Join(stop_times_trips);

                context.Cache.Add("GTFSJSON.routes", routes, new CacheDependency(routes_path), Cache.NoAbsoluteExpiration, Cache.NoSlidingExpiration, CacheItemPriority.Normal, null);
                context.Cache.Add("GTFSJSON.services", services, new CacheDependency(services_path), Cache.NoAbsoluteExpiration, Cache.NoSlidingExpiration, CacheItemPriority.Normal, null);
                context.Cache.Add("GTFSJSON.stops", stops, new CacheDependency(stops_path), Cache.NoAbsoluteExpiration, Cache.NoSlidingExpiration, CacheItemPriority.Normal, null);
                context.Cache.Add("GTFSJSON.stop_times_trips", stop_times_trips, new CacheDependency(stop_times_trips_path), Cache.NoAbsoluteExpiration, Cache.NoSlidingExpiration, CacheItemPriority.Normal, null);
                context.Cache.Add("GTFSJSON.trips", trips, new CacheDependency(trips_path), Cache.NoAbsoluteExpiration, Cache.NoSlidingExpiration, CacheItemPriority.Normal, null);
            }
        }
        public routes routes { get; set; }
        public services services { get; set; }
        public stops stops { get; set; }
        public stop_times_trips stop_times_trips { get; set; }
        public trips trips { get; set; }
    }
}
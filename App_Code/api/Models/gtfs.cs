using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Web;
using System.Web.Caching;

using Newtonsoft.Json;

namespace api.Models
{
    public class gtfs
    {
        private stop_times_trips stop_times_trips { get; set; }
        public gtfs(HttpContext context)
        {
            var serializer = new Newtonsoft.Json.JsonSerializer();
            calendar_dates = context.Cache["GTFSJSON.calendar_dates"] as Models.calendar_dates;
            routes = context.Cache["GTFSJSON.routes"] as Models.routes;
            services = context.Cache["GTFSJSON.services"] as Models.services;
            stops = context.Cache["GTFSJSON.stops"] as Models.stops;
            stop_times_trips = context.Cache["GTFSJSON.stop_times_trips"] as Models.stop_times_trips;
            trips = context.Cache["GTFSJSON.trips"] as Models.trips;

            if (calendar_dates == null || routes == null || services == null || stops == null || stop_times_trips == null || trips == null)
            {
                var calendar_dates_path = context.Server.MapPath("/parsed/calendar_dates.json");
                var routes_path = context.Server.MapPath("/parsed/routes.json");
                var services_path = context.Server.MapPath("/parsed/calendar.json");
                var stops_path = context.Server.MapPath("/parsed/stops.json");
                var stop_times_trips_path = context.Server.MapPath("/parsed/stop_times.json");
                var trips_path = context.Server.MapPath("/parsed/trips.json");
                calendar_dates = serializer.Deserialize<Models.calendar_dates>(new JsonTextReader(new StreamReader(calendar_dates_path)));
                routes = serializer.Deserialize<Models.routes>(new JsonTextReader(new StreamReader(routes_path)));
                services = serializer.Deserialize<Models.services>(new JsonTextReader(new StreamReader(services_path)));
                stops = serializer.Deserialize<Models.stops>(new JsonTextReader(new StreamReader(stops_path)));
                stop_times_trips = serializer.Deserialize<Models.stop_times_trips>(new JsonTextReader(new StreamReader(stop_times_trips_path)));
                trips = serializer.Deserialize<Models.trips>(new JsonTextReader(new StreamReader(trips_path)));

                calendar_dates.Join(services);
                stop_times_trips.Join(stops);
                trips.Join(routes);
                trips.Join(services);
                trips.Join(stop_times_trips);

                context.Cache.Add("GTFSJSON.calendar_dates", calendar_dates, new CacheDependency(calendar_dates_path), Cache.NoAbsoluteExpiration, Cache.NoSlidingExpiration, CacheItemPriority.Normal, null);
                context.Cache.Add("GTFSJSON.routes", routes, new CacheDependency(routes_path), Cache.NoAbsoluteExpiration, Cache.NoSlidingExpiration, CacheItemPriority.Normal, null);
                context.Cache.Add("GTFSJSON.services", services, new CacheDependency(services_path), Cache.NoAbsoluteExpiration, Cache.NoSlidingExpiration, CacheItemPriority.Normal, null);
                context.Cache.Add("GTFSJSON.stops", stops, new CacheDependency(stops_path), Cache.NoAbsoluteExpiration, Cache.NoSlidingExpiration, CacheItemPriority.Normal, null);
                context.Cache.Add("GTFSJSON.stop_times_trips", stop_times_trips, new CacheDependency(stop_times_trips_path), Cache.NoAbsoluteExpiration, Cache.NoSlidingExpiration, CacheItemPriority.Normal, null);
                context.Cache.Add("GTFSJSON.trips", trips, new CacheDependency(trips_path), Cache.NoAbsoluteExpiration, Cache.NoSlidingExpiration, CacheItemPriority.Normal, null);
            }
        }
        public calendar_dates calendar_dates { get; set; }
        public routes routes { get; set; }
        public services services { get; set; }
        public stops stops { get; set; }
        public trips trips { get; set; }
    }
}
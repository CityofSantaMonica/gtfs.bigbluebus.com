/*
Example real-time bus location map
*/
var map;
var bounds = new google.maps.LatLngBounds();
var markers = [];
var mapLabels = [];
var infoWindow = new google.maps.InfoWindow({ content: "" });
var ProtoBuf = dcodeIO.ProtoBuf;
var transit_realtime = ProtoBuf.loadProtoFile("javascript-protobuf/gtfs-realtime.proto").build('transit_realtime'); // "transit_realtime" is the package name inside the proto file
var initialPoisition = false;
var VehiclePositionsFeedMessage;
var TripUpdatesFeedMessage;
// these variables will have the GTFS JSON data
var routes;
var trips;
var stops;
var stop_times;

function sendRequest(path, responseType, handler) {
    var xhr = ProtoBuf.Util.XHR(); // browser specific XHR
    xhr.open("GET", path, true);
    xhr.responseType = responseType;
    xhr.onload = handler;
    xhr.send(null);
}
function getTripUpdateDelay(entity_id, trip_id) {
    for (var index in TripUpdatesFeedMessage.entity) {
        var entity = TripUpdatesFeedMessage.entity[index];
        if (entity.id == entity_id && entity.trip_update.trip.trip_id == trip_id) {
            return -(entity.trip_update.stop_time_update[0].arrival.delay / 60); // invert delay time so that it represents ahead or behind schedule
        }
    }
}
function getVehiclePosition(index) {
    var entity = VehiclePositionsFeedMessage.entity[index];
    var trip = trips[entity.vehicle.trip.trip_id];
    var route = routes[trip.route_id];
    var stop_time = stop_times == undefined ? undefined : stop_times[trip.trip_id];
    var position = entity.vehicle.position;
    var vehicle = entity.vehicle.vehicle;
    var delay = getTripUpdateDelay(entity.id, trip.trip_id);
    return { position: position, vehicle: vehicle, trip: trip, route: route, delay: delay, stop_time: stop_time };
}
function markVehicles() {
    // clear previous vehicle positions
    while (markers.length > 0) {
        var marker = markers.pop();
        marker.setMap(null)
    }
    // clear previous scheduled stop times (if there were any)
    while (mapLabels.length > 0) {
        var mapLabel = mapLabels.pop();
        mapLabel.setMap(null)
    }
    mapLabels = [];
    for (var index in VehiclePositionsFeedMessage.entity) {
        var VehiclePosition = getVehiclePosition(index);
        var position = VehiclePosition.position;
        var vehicle = VehiclePosition.vehicle;
        var trip = VehiclePosition.trip;
        var route = VehiclePosition.route;
        var delay = VehiclePosition.delay;
        var stop_time = VehiclePosition.stop_time;
        var latLng = new google.maps.LatLng(position.latitude, position.longitude);
        var marker = new google.maps.Marker({
            position: latLng,
            map: map,
            title: route.route_short_name.concat(" - ", trip.trip_headsign, " [", trip.block_id, "] - ", delay == undefined ? vehicle.id : vehicle.id.concat(" (", delay > 0 ? "+" : "", delay, " min)")),
            icon: {
                path: "M 10,5 A 5,5 0 0 1 5,10 5,5 0 0 1 0,5 5,5 0 0 1 5,0 5,5 0 0 1 10,5 Z", // SVG path draws circle that can be filled with route color
                anchor: new google.maps.Point(5, 5),
                size: new google.maps.Size(10, 10),
                origin: new google.maps.Point(5, 5),
                fillColor: "#".concat(route.route_color),
                fillOpacity: 1
            }
        });
        marker.shape_id = trip.shape_id;
        marker.stop_time = stop_time;
        marker.route = route;
        google.maps.event.addListener(marker, 'click', (function (evt) {
            selected_marker = this;
            map.data.setStyle(function (feature) {
                var shape_id = feature.getProperty('shape_id');
                var color = feature.getProperty('route_color');
                return {
                    strokeColor: "#".concat(color),
                    strokeOpacity: 0.66,
                    visible: shape_id == selected_marker.shape_id
                }
            });
            infoWindow.setContent(selected_marker.title);
            infoWindow.open(map, this);
            while (mapLabels.length > 0) {
                var mapLabel = mapLabels.pop();
                mapLabel.setMap(null)
            }
            for (var index in this.stop_time) {
                try {
                    var stop_time = this.stop_time[index];
                    var stop = stops[stop_time.stop_id];
                    var mapLabel = new MapLabel({
                        text: stop_time.arrival_time.substring(0, 5),
                        position: new google.maps.LatLng(stop.stop_lat, stop.stop_lon),
                        map: map,
                        fontSize: 12,
                        align: 'center',
                        fontColor: "#ffffff",
                        strokeColor: "#666666"
                    });
                    mapLabels.push(mapLabel);
                } catch (e) { }
            }
        }));
        bounds.extend(latLng);
        markers.push(marker);
    }
    if (!initialPoisition) {
        map.fitBounds(bounds);
        initialPoisition = true;
    }
};
function getUpdateResponse() {
    // decode the protocol buffers data
    try {
        TripUpdatesFeedMessage = transit_realtime.FeedMessage.decode(this.response);
        // we have all the data needed to update the map
        markVehicles();
    }
    // there is an error in the data, we wait for the next cycle to get fresh data
    catch (e) {

    }
}
function sendUpdateRequest() {
    // this is a protocol buffers file
    sendRequest("tripupdates.bin", "arraybuffer", getUpdateResponse);
}
function getPositionResponse() {
    // decode the protocol buffers data
    try {
        VehiclePositionsFeedMessage = transit_realtime.FeedMessage.decode(this.response);
        sendUpdateRequest();
    }
    // there is an error in the data, we wait for the next cycle to get fresh data
    catch (e) {

    }
}
function sendPositionRequest() {
    // this is a protocol buffers file
    sendRequest("vehiclepositions.bin", "arraybuffer", getPositionResponse);
}
function getStopTimesResponse() {
    try {
        stop_times = JSON.parse(this.responseText);
        // update the page to indicate that scheduled stop times are now available
        var scheduledstoptimesmessage = document.getElementById("scheduledstoptimesmessage");
        scheduledstoptimesmessage.style.display = "inline";
    } catch (e) { }
}
function sendStopTimesRequest() {
    // this will take some time...
    sendRequest("parsed/stop_times.json", "text", getStopTimesResponse);
}
function getStopsResponse() {
    try {
        stops = JSON.parse(this.responseText);
        sendStopTimesRequest();
    } catch (e) { }
}
function sendStopsRequest() {
    sendRequest("parsed/stops.json", "text", getStopsResponse);
}
function getTripsResponse() {
    try {
        trips = JSON.parse(this.responseText);
        // if not Android or iPhone, request stops and stop_times
        if (!(navigator.userAgent.match(/Android/i) || navigator.userAgent.match(/iPhone/i)))
            sendStopsRequest();
        // start requesting GTFS real time protocol buffers 
        sendPositionRequest();
        window.setInterval(function () {
            // repeat this every 20 seconds
            sendPositionRequest();
        }, 20000);
    } catch (e) { }
}
function sendTripsRequest() {
    sendRequest("parsed/trips.json", "text", getTripsResponse);
}
function getRoutesResponse() {
    try {
        routes = JSON.parse(this.responseText);
        sendTripsRequest();
    } catch (e) { }
}
function sendRoutesRequest() {
    sendRequest("parsed/routes.json", "text", getRoutesResponse);
}
function initialize() {
    // create Google Map
    map = new google.maps.Map(document.getElementById("example-map"), { center: new google.maps.LatLng(34.013776, -118.492043), zoom: 15 });
    // load GeoJSON of routes to be shown when bus is selected
    map.data.loadGeoJson('/parsed/shapes.geojson', null, function () {
        map.data.setStyle(function (feature) {
            var color = feature.getProperty('route_color');
            return {
                strokeColor: "#".concat(color),
                visible: false
            }
        });
    });
    // use transit layer to provider better color contrast with transit routes
    var transitLayer = new google.maps.TransitLayer();
    transitLayer.setMap(map);
    // begin requests for JSON files: routes, trips, stops, stop_times
    // work your way up this JavaScript file for the rest of the process
    sendRoutesRequest();
}
google.maps.event.addDomListener(window, 'load', initialize);

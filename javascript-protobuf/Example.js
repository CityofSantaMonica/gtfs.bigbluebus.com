/*
Example real-time bus location map
*/
var map;
var bounds = new google.maps.LatLngBounds();
var markers = new Set();
var infoWindow = new google.maps.InfoWindow({ content: "" });
var ProtoBuf = dcodeIO.ProtoBuf;
var transit_realtime = ProtoBuf.loadProtoFile("javascript-protobuf/gtfs-realtime.proto").build('transit_realtime');
var xhr;
var initialPoisition = false;
var routes;
var trips;
var VehiclePositionsFeedMessage;
var TripUpdatesFeedMessage;
function sendRequest(path, responseType, handler) {
    xhr = ProtoBuf.Util.XHR();
    xhr.open("GET", path, true);
    xhr.responseType = responseType;
    xhr.onload = handler;
    xhr.send(null);
}
function getTripUpdateDelay(entity_id, trip_id) {
    for (var index in TripUpdatesFeedMessage.entity) {
        var entity = TripUpdatesFeedMessage.entity[index];
        if (entity.id == entity_id && entity.trip_update.trip.trip_id == trip_id) {
            return entity.trip_update.stop_time_update[0].arrival.delay / 60;
        }
    }
}
function getVehiclePosition(index) {
    var entity = VehiclePositionsFeedMessage.entity[index];
    var trip = trips[entity.vehicle.trip.trip_id];
    var route = routes[trip.route_id];
    var position = entity.vehicle.position;
    var vehicle = entity.vehicle.vehicle;
    var delay = getTripUpdateDelay(entity.id, trip.trip_id);
    return { position: position, vehicle: vehicle, trip: trip, route: route, delay: delay };
}
function markVehicles() {
    markers.forEach(function (marker) {
        marker.setMap(null);
    });
    for (var index in VehiclePositionsFeedMessage.entity) {
        var VehiclePosition = getVehiclePosition(index);
        var position = VehiclePosition.position;
        var vehicle = VehiclePosition.vehicle;
        var trip = VehiclePosition.trip;
        var route = VehiclePosition.route;
        var delay = VehiclePosition.delay;
        var latLng = new google.maps.LatLng(position.latitude, position.longitude);
        var marker = new google.maps.Marker({
            position: latLng,
            map: map,
            title: route.route_short_name.concat(" - ", delay == undefined ? vehicle.id : vehicle.id.concat(" (", delay > 0 ? "+" : "", delay, " min)")),
            icon: {
                path: "M 10,5 A 5,5 0 0 1 5,10 5,5 0 0 1 0,5 5,5 0 0 1 5,0 5,5 0 0 1 10,5 Z",
                anchor: new google.maps.Point(5, 5),
                size: new google.maps.Size(10, 10),
                origin: new google.maps.Point(5, 5),
                fillColor: "#".concat(route.route_color),
                fillOpacity: 1
            }
        });
        marker.shape_id = trip.shape_id;
        google.maps.event.addListener(marker, 'click', (function (evt) {
            selected_shape = this;
            map.data.setStyle(function (feature) {
                var shape_id = feature.getProperty('shape_id');
                var color = feature.getProperty('route_color');
                return {
                    strokeColor: "#".concat(color),
                    visible: shape_id == selected_shape.shape_id
                }
            });
            infoWindow.setContent (selected_shape.title);
            infoWindow.open(map, this);
        }));
        bounds.extend(latLng);
        markers.add(marker);
    }
    if (!initialPoisition) {
        map.fitBounds(bounds);
        initialPoisition = true;
    }
};
function getUpdateResponse() {
    try {
        TripUpdatesFeedMessage = transit_realtime.FeedMessage.decode(xhr.response);
        markVehicles();
    }
    catch (e) {

    }
}
function sendUpdateRequest() {
    sendRequest("tripupdates.bin", "arraybuffer", getUpdateResponse);
}
function getPositionResponse() {
    try {
        VehiclePositionsFeedMessage = transit_realtime.FeedMessage.decode(xhr.response);
        sendUpdateRequest();
    }
    catch (e) {

    }
}
function sendPositionRequest() {
    sendRequest("vehiclepositions.bin", "arraybuffer", getPositionResponse);
}
function getTripsResponse() {
    trips = JSON.parse(xhr.responseText);
    sendPositionRequest();
    window.setInterval(function () {
        sendPositionRequest();
    }, 20000);
}
function sendTripsRequest() {
    sendRequest("parsed/trips.json", "text", getTripsResponse);
}
function getRoutesResponse() {
    routes = JSON.parse(xhr.responseText);
    sendTripsRequest();
}
function sendRoutesRequest() {
    sendRequest("parsed/routes.json", "text", getRoutesResponse);
}
function initialize() {
    map = new google.maps.Map(document.getElementById("example-map"), { center: new google.maps.LatLng(34.013776, -118.492043), zoom: 15 });
    map.data.loadGeoJson('http://gtfs.bigbluebus.com/parsed/shapes.geojson', null, function () {
        map.data.setStyle(function (feature) {
            var color = feature.getProperty('route_color');
            return {
                strokeColor: "#".concat(color),
                visible: false
            }
        });
    });
    var transitLayer = new google.maps.TransitLayer();
    transitLayer.setMap(map);
    sendRoutesRequest();
}
google.maps.event.addDomListener(window, 'load', initialize);

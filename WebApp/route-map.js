/// <reference path="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-1.11.3.js" />
var host_url;
var route_short_name;
var show_arrows;
var map;
var infoWindow = new google.maps.InfoWindow({ content: "" });
var schedules;
var stops;
var markers = [];
var polylines = [];
var infowindow
var mapResized = false;
function loadMap() {
    infoWindow.close();
    $schedule = $("#route-map-schedule").val();
    $service = $("#route-map-day-of-week").val();
    $direction = $("#route-map-direction").val();
    var services = schedules[$schedule];
    var service = services[$service];
    var route = service.route;
    var direction = service.directions[$direction];
    var markerIcon = { fillColor: "#".concat(route.route_color), fillOpacity: 1, path: 'M 5,0 A 5,5 0 0 1 0,5 5,5 0 0 1 -5,0 5,5 0 0 1 0,-5 5,5 0 0 1 5,0 Z' };
    map.data.setStyle(function (feature) {
        var shape_id = feature.getProperty('shape_id');
        var visible = false;
        for (var index in direction.shape_ids)
            if (direction.shape_ids[index] == shape_id) {
                if (show_arrows === false)
                    visible = true;
            }
        return {
            strokeColor: "#".concat(route.route_color),
            strokeOpacity: 1,
            visible: visible
        }
    });
    var bounds = new google.maps.LatLngBounds();
    while (markers.length > 0) {
        var marker = markers.pop();
        marker.setMap(null)
    }

    while (polylines.length > 0) {
        var polyline = polylines.pop();
        polyline.setMap(null);
    }
    map.data.forEach(function (feature) {
        var route_id = feature.getProperty('route_id');
        var service_id = feature.getProperty('service_id');
        var direction_id = feature.getProperty('direction_id');
        var route_color = feature.getProperty('route_color');
        if (route.route_id == route_id && $service == service_id && $direction == direction_id) {
            var multi_line_string = feature.getGeometry();
            multi_line_string.getArray().forEach(function (line_string) {
                var vertices = [];
                line_string.getArray().forEach(function (point) {
                    vertices.push(point);
                });
                var polyline = new google.maps.Polyline({
                    path: vertices,
                    strokeColor: '#'.concat(route_color),
                    strokeOpacity: 1.0,
                    strokeWeight: 2
                });
                if (show_arrows)
                    polyline.setOptions({
                        icons: [{icon: { path: 'M 6,-5 10,0 7,0 7,5 5,5 5,0 2,0 Z', fillColor: '#000000', fillOpacity: 1, strokeColor: "#FFFFFF", strokeWeight: 1 }, offset: '0', repeat: '100px' }]
                    });
                polylines.push(polyline);
            });
        }
    });
    for (var index = 0; index < polylines.length; index++)
        polylines[index].setMap(map);

    for (var index in direction.stop_ids) {
        var stop = stops[direction.stop_ids[index]];
        var latLng = new google.maps.LatLng(stop.stop_lat, stop.stop_lon);
        var marker = new google.maps.Marker({
            position: latLng,
            map: map,
            title: stop.stop_name,
            icon: markerIcon,
            service_id: service.service_id,
            route_id: route.route_id,
            direction_id: direction.direction_id,
            stop_id: direction.stop_ids[index]
        });
        google.maps.event.addListener(marker, 'click', function () {
            map.setOptions({
                draggableCursor: 'wait'
            });
            var service_id = this.service_id;
            var route_id = this.route_id;
            var direction_id = this.direction_id;
            var stop_id = this.stop_id;
            infoWindow.close();
            infoWindow.setPosition(this.position);
            jQuery.ajax(host_url + "/stops/" + stop_id + "/stop_times/" + service_id + "/" + route_id + "/" + direction_id, {
                complete: function (jqXHR, textStatus) {
                    if (textStatus == "success") {
                        map.setOptions({
                            draggableCursor: 'auto'
                        });
                        stop_info = jqXHR.responseJSON;
                        infoWindow.setContent(stop_info.stop_times_html);
                        infoWindow.open(map);
                    }
                },
                dataType: "json"
            });


        });
        markers.push(marker);
        bounds.extend(latLng);
    }
    if (!mapResized) {
        map.fitBounds(bounds);
        mapResized = true;
    }
    map.setOptions({
        draggableCursor: 'auto'
    });

}
function loadDirections() {
    infoWindow.close();
    $schedule = $("#route-map-schedule").val();
    $service = $("#route-map-day-of-week").val();
    $direction = $("#route-map-direction");
    $direction.empty();
    var services = schedules[$schedule];
    var service = services[$service];
    var directions = service.directions;
    for (var direction_key in directions) {
        var direction = directions[direction_key];
        $option = $("<option>").text(direction.trip_headsign).attr("value", direction.direction_id);
        $direction.append($option);
    }
    $direction.change(loadMap);
    loadMap();
}
function loadWeekDays() {
    infoWindow.close();
    $schedule = $("#route-map-schedule").val();
    $service = $("#route-map-day-of-week");
    $service.empty();
    var services = schedules[$schedule];
    for (var service_key in services) {
        var service = services[service_key];
        $option = $("<option>");
        var today = new Date();
        var dayOfWeek = today.getDay();
        switch (dayOfWeek) {
            case 0:
                if (service.sunday)
                    $option.attr("selected", "selected");
                break;
            case 1:
                if (service.monday)
                    $option.attr("selected", "selected");
                break;
            case 2:
                if (service.tuesday)
                    $option.attr("selected", "selected");
                break;
            case 3:
                if (service.wednesday)
                    $option.attr("selected", "selected");
                break;
            case 4:
                if (service.thursday)
                    $option.attr("selected", "selected");
                break;
            case 5:
                if (service.friday)
                    $option.attr("selected", "selected");
                break;
            case 6:
                if (service.saturday)
                    $option.attr("selected", "selected");
                break;
        }
        $option.text(service.name);
        $option.attr("value", service.service_id);
        $service.append($option);
    }
    $service.change(loadDirections);
    loadDirections();
}
function createRouteMap(hostUrl, routeShortName, showArrows) {
    // create Google Map
    host_url = hostUrl;
    route_short_name = routeShortName;
    if (showArrows == undefined)
        show_arrows = false;
    else
        show_arrows = showArrows;
    var route_map = document.getElementById("route-map");
    map = new google.maps.Map(route_map, { center: new google.maps.LatLng(34.013776, -118.492043), zoom: 12, draggableCursor: 'wait', styles: [{ "featureType": "transit.station.bus", "elementType": "labels.icon", "stylers": [{ "visibility": "off" }] }] });
    // load GeoJSON of routes to be shown when bus is selected
    // use transit layer to provider better color contrast with transit routes
    var transitLayer = new google.maps.TransitLayer();
    transitLayer.setMap(map);
    // begin requests for files
    map.data.loadGeoJson(host_url + "/parsed/traces.geojson", null, function () {
        map.data.setStyle(function (feature) {
            var color = feature.getProperty('route_color');
            return {
                strokeColor: "#".concat(color),
                visible: false
            }
        });
        jQuery.ajax(host_url + "/stops", {
            complete: function (jqXHR, textStatus) {
                if (textStatus == "success") {
                    stops = jqXHR.responseJSON;
                    jQuery.ajax(host_url + "/map-info/" + route_short_name, {
                        complete: function (jqXHR, textStatus) {
                            if (textStatus == "success") {
                                schedules = jqXHR.responseJSON;
                                var today = new Date();
                                var $schedule = $("#route-map-schedule");
                                for (schedule_key in schedules) {
                                    $option = $("<option>");
                                    var services = schedules[schedule_key];
                                    for (var service_key in services) {
                                        var service = services[service_key];
                                        var start_date = new Date(service.start_date);
                                        var end_date = new Date(service.end_date);
                                        if (start_date <= today && end_date >= today)
                                            $option.attr("selected", "selected");
                                    }
                                    $option.text(schedule_key);
                                    $schedule.append($option);
                                }
                                if ($schedule.children('option').length == 1) {
                                    $("#schedule-dropdown-message").css("visibility", "hidden");
                                }
                                else {
                                    $("#schedule-dropdown-message").css("visibility", "visible");
                                }
                                $schedule.change(loadWeekDays);
                                loadWeekDays();
                            }
                        },
                        dataType: "json"
                    });
                }
            },
            dataType: "json"
        });
    });
}

//Set map height based on width 
var SetMapHeight = function() {
    var div = $('#map');
    var width = div.width();
    div.css('height', Math.max(width / 3, 500));
};

//Create Map
var createMap = function(location = [-96.8, 32.75]) {
    mapboxgl.accessToken = 'pk.eyJ1Ijoiam9uYXRoYW4tay1zdWxsaXZhbiIsImEiOiJja3JqdXhscjYwb2dlMm9xcmh0anQyZzFiIn0.vFh9AmMWbr6PGBVBDHkp8Q';
    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/dark-v10?optimize=true',
        center: location, // starting position,
        zoom: 9.5
    });
    return map;
};

// Add geolocate control to the map.
var createMapWithGeoLocation = function() {
    if ("geolocation" in navigator) {
        //check geolocation available 
        //try to get user current location using getCurrentPosition() method
        navigator.geolocation.getCurrentPosition(function(position) {
            return createMap([position.coords.latitude,
                position.coords.longitude
            ]);
        });
    } else {
        return createMap();
    }
};

var createPopup = function(message, marker) {
    new mapboxgl.Popup({
            className: 'my-machines'
        })
        .setHTML("message>")
        .setMaxWidth("300px")
        .addTo(marker);
};

var setPlaces = function(map, features) {
    map.addSource('places', {
        // This GeoJSON contains features that include an "icon"
        // property. The value of the "icon" property corresponds
        // to an image in the Mapbox Streets style's sprite.
        'type': 'geojson',
        'data': {
            'type': 'FeatureCollection',
            'features': features
        }
    });
};


var addPlacesLayer = function(map) {
    // Add a layer showing the places.
    map.addLayer({
        'id': 'places',
        'type': 'symbol',
        'source': 'places',
        'layout': {
            'icon-image': '{icon}',
            'icon-allow-overlap': true,
            'icon-size': 2
        }
    });
};

var setUpMapMouseSetting = function(map) {
    // When a click event occurs on a feature in the places layer, open a popup at the
    // location of the feature, with description HTML from its properties.
    map.on('click', 'places', function(e) {
        var coordinates = e.features[0].geometry.coordinates.slice();
        var description = e.features[0].properties.description;

        // Ensure that if the map is zoomed out such that multiple
        // copies of the feature are visible, the popup appears
        // over the copy being pointed to.
        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
            coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
        }

        new mapboxgl.Popup()
            .setLngLat(coordinates)
            .setHTML(description)
            .addTo(map);
    });

    // Change the cursor to a pointer when the mouse is over the places layer.
    map.on('mouseenter', 'places', function() {
        map.getCanvas().style.cursor = 'pointer';
    });

    // Change it back to a pointer when it leaves.
    map.on('mouseleave', 'places', function() {
        map.getCanvas().style.cursor = '';
    });
};

var createFeatures = function(locations) {
    var features = [];
    for (var i = 0; i < locations.length; i += 1) {
        var feature = {
            'type': 'Feature',
            'properties': {
                'description': '<a href="#location-' + locations[i].id + '"><strong>' + locations[i].name + '</strong><p>' + locations[i].location.address1 + '</p></a><p>' + locations[i].description + '</p>',
                'icon': 'bar-15'
            },
            'geometry': {
                'type': 'Point',
                'coordinates': [locations[i].location.coordinates.longitude,
                    locations[i].location.coordinates.latitude
                ]
            }
        };
        features.push(feature);
    }
    return features;
};

var getDIstance = function(lat1, lon1, lat2, lon2, unit) {
    if ((lat1 == lat2) && (lon1 == lon2)) {
        return 0;
    } else {
        var radlat1 = Math.PI * lat1 / 180;
        var radlat2 = Math.PI * lat2 / 180;
        var theta = lon1 - lon2;
        var radtheta = Math.PI * theta / 180;
        var dist = Math.sin(radlat1) * Math.sin(radlat2) + Math.cos(radlat1) * Math.cos(radlat2) * Math.cos(radtheta);
        if (dist > 1) {
            dist = 1;
        }
        dist = Math.acos(dist);
        dist = dist * 180 / Math.PI;
        dist = dist * 60 * 1.1515;
        if (unit == "K") {
            dist = dist * 1.609344;
        }
        if (unit == "N") {
            dist = dist * 0.8684;
        }
        return dist;
    }
};

var g_pos;

var error = function(e) {
    alert(e);
    var locations = data.sort(function compareFn(firstEl, secondEl) {
        var dist1 = getDIstance(32.7767, -96.7970,
            firstEl.location.coordinates.lattitude,
            firstEl.location.coordinates.longitude);
        var dist2 = getDIstance(32.7767, -96.7970,
            secondEl.location.coordinates.lattitude,
            secondEl.location.coordinates.longitude);
        return dist1 - dist2;
    });

    var map = createMap();

    var features = createFeatures(locations);
    map.on('load', function() {
        setPlaces(map, features);
    });
    map.on('load', function() {
        addPlacesLayer(map);
    });

    // Set up Hover and Click functionallity
    setUpMapMouseSetting(map);
};

var success = function(pos) {
    var crd = pos.coords;
    g_pos = pos; // assign to global
    var locations = data.locations.sort(function compareFn(firstEl, secondEl) {
        var dist1 = getDIstance(32.7767, -96.7970,
            firstEl.location.coordinates.lattitude,
            firstEl.location.coordinates.longitude);
        var dist2 = getDIstance(32.7767, -96.7970,
            secondEl.location.coordinates.lattitude,
            secondEl.location.coordinates.longitude);
        return dist1 - dist2;
    });

    var map = createMap();

    var features = createFeatures(locations);
    map.on('load', function() {
        setPlaces(map, features);
    });
    map.on('load', function() {
        addPlacesLayer(map);
    });

    $("#locator-listview").empty();
    for (var i = 0; i < locations.length; i++) {
        var location = locations[i];
        var info_html = '';
    
        info_html = info_html + '<div class="row"> \
									<div class="col-xs-12"> \
										<span>' + location.description + '</span> \
									</div> \
								</div> \
								<br/>';
    


        $("#locator-listview").append('<li> \
				  	<div id="location-' + location.id + '" class="col-xs-12"> \
					<h2 class="display-2">' + location.name + '</h2> \
					<div class="row"> \
						<div class="col-xs-12 col-md-6 col-lg-3"> \
							<img src="' + location.image + '" class="img-thumbnail img-fluid  mx-auto d-bloc"> \
						</div> \
						<div class="col-xs-12 col-md-6 col-lg-9">' +
            info_html +
            '<br/><a href="' + location.direction_link + '" class="btn tn-primary mx-5"> <i class="fas fa-directions mx-3"> Directions to this location </i></a> \
			       </div> \
				    </div> \
				</div> \
	  	</li>');
    }

    // Set up Hover and Click functionallity
    setUpMapMouseSetting(map);
};

var options = {
    enableHighAccuracy: true,
    timeout: 5000,
    maximumAge: 0
};
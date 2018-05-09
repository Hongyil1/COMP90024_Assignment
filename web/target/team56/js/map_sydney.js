var censusMin = Number.MAX_VALUE, censusMax = -Number.MAX_VALUE;

/**
 * Set properties of google maps
 */
var mapStyle = [ {
	'stylers' : [ {
		'visibility' : 'on'
	} ]
}, {
	'featureType' : 'landscape',
	'elementType' : 'geometry',
	'stylers' : [ {
		'visibility' : 'on'
	}, {
		'color' : '#fcfcfc'
	} ]
}, {
	'featureType' : 'water',
	'elementType' : 'geometry',
	'stylers' : [ {
		'visibility' : 'on'
	}, {
		'color' : '#bfd4ff'
	} ]
} ];

function initMap() {
	// load the map
	map = new google.maps.Map(document.getElementById('map'), {
		center : {
			lat : -33.862,
			lng : 150.8
		},
		zoom :10,
		styles : mapStyle
	});

	map.data.setStyle(styleFeature);
	map.data.addListener('mouseover', mouseInToRegion);
	map.data.addListener('mouseout', mouseOutOfRegion);
	map.data.addListener('click', showDetailData);

	loadMapShapes();
}

/** Loads the state boundary polygons from a GeoJSON source. */
function loadMapShapes() {
	// load US state outline polygons from a GeoJson file
	map.data.loadGeoJson('data/sydney.json', {
		idPropertyName : 'loc_pid'
	});
}

/**
 * Applies a gradient style based on the 'census_variable' column. This is the
 * callback passed to data.setStyle() and is called for each row in the data
 * set. Check out the docs for Data.StylingFunction.
 * 
 * @param {google.maps.Data.Feature}
 *            feature
 */
function styleFeature(feature) {
	var low = [ 5, 69, 54 ]; // color of smallest datum
	var high = [ 151, 83, 34 ]; // color of largest datum

	// delta represents where the value sits between the min and max
	// var delta = (Math.random() - censusMin) / (censusMax - censusMin);

	var delta = Math.random();
	// console.log("#delta:" + delta);
	console.log("suburb name: " + feature.getProperty('loc_pid'));

	var color = [];
	for (var i = 0; i < 3; i++) {
		// calculate an integer color based on the delta
		color[i] = (high[i] - low[i]) * delta + low[i];
	}

	// determine whether to show this shape or not
	var showRow = true;

	var outlineWeight = 0.5, zIndex = 1;
	if (feature.getProperty('loc_pid') === 'hover') {
		outlineWeight = zIndex = 2;
	}

	return {
		strokeWeight : outlineWeight,
		strokeColor : '#fff',
		zIndex : zIndex,
		fillColor : 'hsl(' + color[0] + ',' + color[1] + '%,' + color[2] + '%)',
		fillOpacity : 0.75,
		visible : showRow
	};
}

/**
 * Responds to the mouse-in event on a map shape (state).
 * 
 * @param {?google.maps.MouseEvent}
 */
function mouseInToRegion(e) {
	// set the hover state so the setStyle function can change the border
	e.feature.setProperty('loc_pid', 'hover');
}

/**
 * Responds to the mouse-out event on a map shape (state).
 * 
 * @param {?google.maps.MouseEvent}
 *            e
 */
function mouseOutOfRegion(e) {
	// reset the hover state, returning the border to normal
	e.feature.setProperty('loc_pid', 'normal');
}

function showDetailData(e) {
	document.getElementById('light').style.display = 'block';
	document.getElementById('fade').style.display = 'block';
}
;
// map center. Default is Cidade Nova
var myLatlng = new google.maps.LatLng(-22.86557808, -43.22364807);
// map options,
var myOptions = {
  zoom: 12,
  center: myLatlng
};
// standard map
map = new google.maps.Map(document.getElementById("map"), myOptions);
// heatmap layer
heatmap = new HeatmapOverlay(map, 
  {
    // radius should be small ONLY if scaleRadius is true (or small radius is intended)
    "radius": 10,
    "maxOpacity": 1,
    "scaleRadius": false,
    "useLocalExtrema": false,
    latField: 'lat',
    lngField: 'lng',
    valueField: 'value',
    dissipating: false,
    maxIntensity: 12000,
  }
);

markers = []


// Sets the map on all markers in the array.
function setMapOnAll(map) {
    for (var i = 0; i < markers.length; i++) {
      markers[i].setMap(map);
    }
}

// Removes the markers from the map, but keeps them in the array.
function clearMarkers() {
    setMapOnAll(null);
}

// Shows any markers currently in the array.
function showMarkers() {
    setMapOnAll(map);
}

// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
    clearMarkers();
    markers = [];
}


var frm = $('#visualization-search');
frm.submit(function () {
    console.log(frm);
    console.log(frm.serialize());
    $.ajax({
        type: frm.attr('method'),
        url: frm.attr('action'),
        data: frm.serialize(),
        success: function (data) {
            console.log("Data:");
            console.log(data);
            heatmap.setData(data);
            heatmap.set('dissipating', false);
            var infowindow = new google.maps.InfoWindow();

            function placeMarker(info){

                var contentString = '<div id="content">'+
                    '<div id="siteNotice">'+
                    '</div>'+
                    '<div id="bodyContent">'+
                    '<p><b>Time: </b><p>' + info.time + '</p>' +
                    '<p><b>Temperature: </b><p>' + info.temperature + ' C</p>' +
                    '<p><b>Humidity: </b><p>' + info.humidity + ' %</p>' +
                    '<p><b>Rain: </b><p>' + info.rain + '</p>' +
                    '<p><b>Light intensity: </b><p>' + info.light + '</p>' +
                    '</div>'+
                    '</div>';


                var marker = new google.maps.Marker({
                    position: new google.maps.LatLng(info.lat, info.lng),
                    icon: {
                        path: google.maps.SymbolPath.CIRCLE,
                        strokeColor: '#FF0000',
                        strokeOpacity: 0,
                        strokeWeight: 1,
                        fillColor: '#FF0000',
                        fillOpacity: 0,
                        scale: 3
                    },
                    map: map,
                });

                google.maps.event.addListener(marker, 'click', function(){
                    infowindow.close(); // Close previously opened infowindow
                    infowindow.setContent(contentString);
                    infowindow.open(map, marker);
                });

                markers.push(marker);
            }
            //Here we draw markers
            for (var i = 0; i < data.data.length; i++){
                placeMarker(data.data[i])
            }
        },
        error: function(data) {
            console.log("Something went wrong!");
        }
    });
    return false;
});
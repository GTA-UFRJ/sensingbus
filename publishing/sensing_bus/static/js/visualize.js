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
    valueField: 'value'
  }
);


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
            //Here we draw circles.
            for (var i = 0; i < data.data.length; i++){

                var contentString = '<div id="content">'+
                    '<div id="siteNotice">'+
                    '</div>'+
                    '<div id="bodyContent">'+
                    '<p><b>Temperature: </b><p>' + data.data[i].temperature + '</p>' +
                    '<p><b>Humidity: </b><p>' + data.data[i].humidity + '</p>' +
                    '<p><b>Rain: </b><p>' + data.data[i].rain + '</p>' +
                    '<p><b>Light intensity: </b><p>' + data.data[i].light + '</p>' +
                    '</div>'+
                    '</div>';
                var infowindow = new google.maps.InfoWindow({
                  content: contentString
                });

                var marker = new google.maps.Marker({
                    position: new google.maps.LatLng(data.data[i].lat, data.data[i].lng),
                    icon: {
                        path: google.maps.SymbolPath.CIRCLE,
                        strokeColor: '#FF0000',
                        strokeOpacity: 0,
                        strokeWeight: 1,
                        fillColor: '#FF0000',
                        fillOpacity: 1,
                        scale: 3
                    },
                    map: map,
                });

                marker.addListener('click', function() {
                    infowindow.open(map, marker);
                });
                /*var measurementCircle = new google.maps.Circle({
                    strokeColor: '#FF0000',
                    strokeOpacity: 0.8,
                    strokeWeight: 2,
                    fillColor: '#FF0000',
                    fillOpacity: 0.35,
                    map: map,
                    center: new google.maps.LatLng(data.data[i].lat, data.data[i].lng),
                    radius: 5
                });

                measurementCircle.addListener('click', function() {
                    infowindow.setPosition(measurementCircle.getCenter());
                    infowindow.open(map, measurementCircle);
                });*/
            }
        },
        error: function(data) {
            console.log("Something went wrong!");
        }
    });
    return false;
});
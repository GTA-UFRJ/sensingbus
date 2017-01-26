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
            console.log(data.data);
            heatmap.setData(data);
        },
        error: function(data) {
            console.log("Something went wrong!");
        }
    });
    return false;
});
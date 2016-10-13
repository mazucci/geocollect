//console.log(fsq_categories.data[0].fsq_category);
//console.log(fsq_categories.data.length);
for (var m=0; m<fsq_categories.data.length; m++){
  $('#select_fsq').append($('<option>', {
       value: fsq_categories.data[m].fsq_category,
       text : fsq_categories.data[m].fsq_category
   }));
}

var twtLayer, fsqLayer, map;

var baseDark = L.tileLayer("http://{s}.api.cartocdn.com/{styleId}/{z}/{x}/{y}.png", {
  styleId: "base-dark",
  attribution: 'CartoDB base map, data from <a href="http://openstreetmap.org">OpenStreetMap</a>'
});

var baseLight = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
	subdomains: 'abcd',
	maxZoom: 19
});

var cfg_twt = {
  "radius": .02,
  "maxOpacity": .5,
  "scaleRadius": true,
  "useLocalExtrema": true,
  latField: 'lat',
  lngField: 'lng',
  valueField: 'count',
  gradient: {
    '.4': '#ccff33',
    '.8': '#ffff00',
    '.95': '#ff9900',
    '1': '#ff531a'
  }
};
twtLayer = new HeatmapOverlay(cfg_twt);

var cfg_fsq = {
  "radius": .02,
  "maxOpacity": .7,
  "scaleRadius": true,
  "useLocalExtrema": true,
  latField: 'lat',
  lngField: 'lng',
  valueField: 'count',
  gradient: {
    '.4': '#00ffcc',
    '.8': '#00ff99',
    '.95': '#00ff00',
    '1': '#00b300'
  }
};
fsqLayer = new HeatmapOverlay(cfg_fsq);

map = new L.Map('map', {
  center: new L.LatLng(45.46, 9.18),
  zoom: 8,
  layers: [baseDark]
});

var urlTWT = "http://geolab.como.polimi.it/heatmap/collector/json/TWT/";
var urlFSQ = "http://geolab.como.polimi.it/heatmap/collector/json/FSQ/";

function getData(url, source) {
  $.get(url, function(data) {
    //console.log(data);
    window[source + "Layer"].setData(data);
    map.addLayer(window[source + "Layer"]);
    map.removeLayer(window[source + "Layer"]);
    map.addLayer(window[source + "Layer"]);
  });
}

getData(urlTWT, "twt");
getData(urlFSQ, "fsq");


function formatDate(date){
  var date_splitted = date.split("/");
  date = date_splitted[1] + "-" + date_splitted[0] + "-" + date_splitted[2];
  return date;
}

$("#date_filter").click(function() {
  if ($('#datepicker_s').val() == '' || $('#datepicker_e').val() == '')
    alert("Please select start and end dates!");
  else {
    var twitter_tag = $('#input_twt').val();
    var fsq_keyword = $('#select_fsq').val();
    var start_date = formatDate($('#datepicker_s').val());
    var end_date = formatDate($('#datepicker_e').val());
    //console.log(start_date + " --- " + end_date + " --- " + twitter_tag + " --- " + fsq_keyword);
    map.removeLayer(twtLayer);
    map.removeLayer(fsqLayer);
    urlTWT = "http://geolab.como.polimi.it/heatmap/collector/json/TWT/" + start_date + "/" + end_date + "/";
    if (twitter_tag != "")
      urlTWT += twitter_tag + "/";
    urlFSQ = "http://geolab.como.polimi.it/heatmap/collector/json/FSQ/" + start_date + "/" + end_date + "/";
    if (fsq_keyword != "")
      urlFSQ += fsq_keyword + "/";
    //console.log(urlTWT + " --- " + urlFSQ);
    getData(urlTWT, "twt");
    getData(urlFSQ, "fsq");
  }
});

$(function(){
  $("#datepicker_s").datepicker({
    maxDate: new Date(),
    onSelect: function(selected){
      $("#datepicker_e").datepicker("option","minDate", selected)
    }
  });
  $("#datepicker_e").datepicker({
    maxDate: new Date(),
    onSelect: function(selected){
      $("#datepicker_s").datepicker("option","maxDate", selected)
    }
  });
});

function chktwt(){
  if($("#twt").is(':checked'))
    map.addLayer(twtLayer);
  else if(!$("#twt").is(':checked'))
    map.removeLayer(twtLayer);
}

function chkfsq(){
  if($("#fsq").is(':checked'))
    map.addLayer(fsqLayer);
  else if(!$("#fsq").is(':checked'))
    map.removeLayer(fsqLayer);
}

$("input[name='base']").click(function() {
  if($("#baseDark").is(':checked')){
    map.addLayer(baseDark);
    map.removeLayer(baseLight);
  }
  else if($("#baseLight").is(':checked')){
    map.addLayer(baseLight);
    map.removeLayer(baseDark);
  }
});

L.DomEvent.disableClickPropagation(L.DomUtil.get('legend'));
L.DomEvent.disableScrollPropagation(L.DomUtil.get('legend'));
L.DomEvent.disableClickPropagation(L.DomUtil.get('filter_settings'));
L.DomEvent.disableScrollPropagation(L.DomUtil.get('filter_settings'));

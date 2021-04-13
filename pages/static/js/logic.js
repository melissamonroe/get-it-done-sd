// Creating map object
var myMap = L.map("map", {
  center: [32.7157, -117.1611],
  zoom: 11
});

// Adding tile layer to the map
L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
  tileSize: 512,
  maxZoom: 18,
  zoomOffset: -1,
  id: "mapbox/streets-v11",
  accessToken: API_KEY
}).addTo(myMap);

const urlParams = new URLSearchParams(window.location.search);

// Store API query variables
var baseURL = "http://127.0.0.1:5104/api/daterequested/";
var year = urlParams.get('year');
var sr_name = "!" + urlParams.get('name');
var limit = "!" + urlParams.get('limit');

console.log(year);

// Assemble API query URL
var url = baseURL + year + sr_name + limit
console.log(url);
// Grab the data with d3
d3.json(url, function(response) {

  // Create a new marker cluster group
  var markers = L.markerClusterGroup();  
  

  // Loop through data
  for (var i = 0; i < response.length; i++) {
      lat = response[i]["lat"]
      lng = response[i]["lng"]
      
      var details = "Service Request ID: " + response[i]["service_request_id"];

      if (response[i]["date_requested"]) {
        details += "<br>Date Requeste: " + response[i]["date_requested"] 
        console.log(response[i]["date_requested"]);
      } if (response[i]["case_age_days"]) { 
        details += "<br>Case Age (days): " + response[i]["case_age_days"] 
      } if (response[i]["service_name"]) {
        details += "<br>Service Name: " + response[i]["service_name"] 
      } if (response[i]["case_record_type"]) {
        details += "<br>Record Type: " + response[i]["case_record_type"] 
      } if (response[i]["date_closed"]) {
        details += "<br>Date Closed: " + response[i]["date_closed"] 
        console.log(response[i]["date_closed"]);
      } if (response[i]["status"]) {
        details += "<br>Status: " + response[i]["status"] 
      } if (response[i]["street_address"]) {
        details += "<br>Street Address: " + response[i]["street_address"] 
      } if (response[i]["council_district"]) {
        details += "<br>Council District: " + response[i]["council_district"] 
      } if (response[i]["comm_plan_code"]) {
        details += "<br>Community Plan Code: " + response[i]["comm_plan_code"] 
      } if (response[i]["comm_plan_name"]) {
        details += "<br>Community Plan Name: " + response[i]["comm_plan_name"] 
      } if (response[i]["case_origin"]) {
        details += "<br>Origin: " + response[i]["case_origin"] 
      } if (response[i]["public_description"]) {
        details += "<br>Description: " + response[i]["public_description"] 
      } if (response[i]["media_url"]) {
        details += "<img src='" + response[i]["media_url"] + "' style='height:200px;float:right'/>";
      }

     // Check for location property
     if ((lat) && (lng)) {
      // Add a new marker to the cluster group and bind a pop-up
      markers.addLayer(L.marker([lat, lng])
        .bindPopup(details));
    }

   }

  // // Add our marker cluster layer to the map
  myMap.addLayer(markers);

});

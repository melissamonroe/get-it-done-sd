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
console.log(year);

// Store API query variables
var baseURL = "http://127.0.0.1:5102/api/daterequested/";
var year = urlParams.get('year');
// var complaint = "&complaint_type=Rodent";
// var limit = "&$limit=100000";
console.log(year);

// Assemble API query URL
var url = baseURL + year;
console.log(url);
// Grab the data with d3
d3.json(url, function(response) {

  // Create a new marker cluster group
  var markers = L.markerClusterGroup();
  
  console.log(response[0]);
  console.log(response[0]["date_closed"]);
  
  

  // Loop through data
  for (var i = 0; i < response.length; i++) {
      
    
    
      lat = response[i]["lat"]
      lng = response[i]["lng"]
      


      var details = "service_request_id: " + response[i]["service_request_id"] + 
                    "<br>date_requested: " + response[i]["date_requested"] +   
                    "<br>case_age_days: " + response[i]["case_age_days"] +
                    "<br>service_name: " + response[i]["service_name"] +
                    "<br>case_record_type: " + response[i]["case_record_type"] +
                    "<br>date_closed: " + response[i]["date_closed"] +
                    "<br>status: " + response[i]["status"] +
                    "<br>street_address: " + response[i]["street_address"] +
                    "<br>council_district: " + response[i]["council_district"] +
                    "<br>comm_plan_code: " + response[i]["comm_plan_code"] +
                    "<br>comm_plan_name: " + response[i]["comm_plan_name"] +
                    "<br>case_origin: " + response[i]["case_origin"] +
                    "<br>public_description: " + response[i]["public_description"];

                    if (response[i]["media_url"]) {
                      details += "<img src='" + response[i]["media_url"] + "' style='height:200px;float:right'/>";
                    }
    //details += "<br/><a href='" + response.features[i].properties.url + "' target='_blank'>USGS Details</a>";
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

console.log("opensrapp")

const url_currentsr = "api/currentsr";
const url_addopensr = "api/addopensr";

function add_open_sr() {
    d3.json(url_addopensr).then(function(response) {

        console.log(url_addopensr);
        
        console.log(response);
      

    });
}

function get_open_sr() {
    d3.json(url_currentsr).then(function(response) {
        console.log(url_currentsr);    
    });
}

get_open_sr();


map_html = "<iframe src='http://127.0.0.1:5500/pages/mapopensr.html?maptype=opensr' height='600px' width='100%' title='Current Service Request Cluster Map'></iframe>";
d3.select("#map").html(map_html)


add_open_sr();
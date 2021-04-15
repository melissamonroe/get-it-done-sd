d3.selectAll("body").on("change", populateDashboard);

function populateServicesNames() {
  url_servicenames = "api/servicenames";
  d3.json(url_servicenames).then(function(response) {
    console.log(response)
    var serviceNameArr = response
    // select inputs 
    var inputElementDate = d3.select("#selServiceName");

    // auto populate available filter days and add blank option to search without date filter
    serviceNameArr.forEach(servicename => {
         inputElementDate.append('option').text(servicename);
    });
  });



  
}

function populateDashboard() {
  console.log("loading summary data...")  
  
  // Use D3 to select the dropdown menu
  var CB_Year = d3.select("#selYear");
  // Assign the value of the dropdown menu option to a variable
  var year = CB_Year.node().value;

  console.log(year);
  
  /* data route */
  const url = "api/summary" + "/" + year;
  d3.json(url).then(function(response) {
    /////////////////////////////////////////////////
    // Multiline Plot SR over time
    /////////////////////////////////////////////////
    console.log(year);
    const data = response[0].summary;
    //console.log(data);

    month = []
    count = []
    for (const [key, value] of Object.entries(data)) {
      // console.log(`${key}: ${value}`);
      month.push(key);
      count.push(value);
    }
    
    countbymonth = [{
      x: month,
      y: count }];
  
    var lineplot = d3.selectAll("#line-plot").node();
  
    Plotly.newPlot(lineplot, countbymonth);
    console.log("Summary data loaded.")


    // bar chart count by service request type
    var chart_url = response[0].chart_url;
    chart_html = "<iframe id='bar-count' style='background: #FFFFFF;border: none;border-radius: 2px;box-shadow: 0 2px 10px 0 rgba(70, 76, 79, .2);' width='100%' height='480' src='" + chart_url + "'></iframe>"
    d3.select("#bar-plot").html(chart_html)

    // bar chart count by council district
    var chart_url_council_dist = response[0].chart_url_council_dist
    chart_council_dist_html = "<iframe id='bar-count' style='background: #FFFFFF;border: none;border-radius: 2px;box-shadow: 0 2px 10px 0 rgba(70, 76, 79, .2);' width='100%' height='480' src='" + chart_url_council_dist + "'></iframe>"
    d3.select("#bar-plot-council-dist").html(chart_council_dist_html)

    var sr_name = "All"
    var limit = 1000
    
    // Use D3 to select the dropdown menu
    var CB_SRName = d3.select("#selServiceName");
    // Assign the value of the dropdown menu option to a variable
    sr_name = CB_SRName.node().value;
    // Use D3 to select the dropdown menu
    var CB_Limit = d3.select("#selMapLimit");
    // Assign the value of the dropdown menu option to a variable
    limit = CB_Limit.node().value;
    console.log(year, sr_name, limit);
  


    map_html = "<iframe src='http://127.0.0.1:5500/pages/index.html?year=" + year + "&name=" + sr_name + "&limit=" + limit + "' height='600px' width='100%' title='Service Request Cluster Map'></iframe>";
    d3.select("#map").html(map_html)
  
    d3.select("#total_requested").html("<span>" + response[0].total_requested + "</span>")
    d3.select("#total_closed").html("<span>" + response[0].total_closed + "</span>")
    d3.select("#percent_closed").html("<span>" + (parseFloat(response[0].percent_closed)*100).toFixed(2).toString() + "%</span>")
    d3.select("#average_case_age").html("<span>" + parseFloat(response[0].average_case_age_days).toFixed(2).toString() + "</span>")

  });
}

function populateDistricts() {
  console.log("loading summary data...")  
  
  // Use D3 to select the dropdown menu
  var CB_District = d3.select("#selDistrict");
  // Assign the value of the dropdown menu option to a variable
  var district = CB_District.node().value;

  console.log(district);
  
  /* data route */
  const cdurl = "api/summary" + "/" + district;
  d3.json(cdurl).then(function(response) {
  
    console.log(district);
    var line_url = response[0].chart_url_cd_tickets_over_time;
    line_html = "<iframe id='bar-count' style='background: #FFFFFF;border: none;border-radius: 2px;box-shadow: 0 2px 10px 0 rgba(70, 76, 79, .2);' width='100%' height='480' src='" + line_url + "'></iframe>"
    d3.select("#cd-line-plot").html(line_html)


    // bar chart count by service request type
    var chart_url = response[0].chart_url;
    chart_html = "<iframe id='bar-count' style='background: #FFFFFF;border: none;border-radius: 2px;box-shadow: 0 2px 10px 0 rgba(70, 76, 79, .2);' width='100%' height='480' src='" + chart_url + "'></iframe>"
    d3.select("#cd-bar-plot").html(chart_html)

    // bar chart count by council district
    var chart_url_council_dist = response[0].chart_url_council_dist
    chart_council_dist_html = "<iframe id='bar-count' style='background: #FFFFFF;border: none;border-radius: 2px;box-shadow: 0 2px 10px 0 rgba(70, 76, 79, .2);' width='100%' height='480' src='" + chart_url_council_dist + "'></iframe>"
    d3.select("#bar-plot-council-dist").html(chart_council_dist_html)

    d3.select("#total_requested").html("<span>" + response[0].total_requested + "</span>")
    d3.select("#total_closed").html("<span>" + response[0].total_closed + "</span>")
    d3.select("#percent_closed").html("<span>" + (parseFloat(response[0].percent_closed)*100).toFixed(2).toString() + "%</span>")
    d3.select("#average_case_age").html("<span>" + parseFloat(response[0].average_case_age_days).toFixed(2).toString() + "</span>")

  });
}

function init() {
  populateServicesNames();
  populateDashboard();
};

init(); 









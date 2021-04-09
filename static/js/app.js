d3.selectAll("body").on("change", populateDashboard);


function populateDashboard() {
  console.log("loading summary data...")  
  
  // Use D3 to select the dropdown menu
  var dropdownMenu = d3.select("#selYear");
  // Assign the value of the dropdown menu option to a variable
  var year = dropdownMenu.node().value;

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

    map_html = "<iframe src='http://127.0.0.1:5500/pages/index.html?" + year + "' height='600px' width='100%' title='Service Request Cluster Map'></iframe>";
    d3.select("#map").html(map_html)
  
    d3.select("#total_requested").html("<span>" + response[0].total_requested + "</span>")
    d3.select("#total_closed").html("<span>" + response[0].total_closed + "</span>")
    d3.select("#percent_closed").html("<span>" + (parseFloat(response[0].percent_closed)*100).toFixed(2).toString() + "%</span>")
    d3.select("#average_case_age").html("<span>" + parseFloat(response[0].average_case_age_days).toFixed(2).toString() + "</span>")

  });
}


populateDashboard();










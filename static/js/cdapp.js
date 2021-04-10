d3.selectAll("body").on("change", populateDistricts);


function populateDistricts() {
  console.log("loading summary data...")  
  
  // Use D3 to select the dropdown menu
  var CB_District = d3.select("#selDistrict");
  // Assign the value of the dropdown menu option to a variable
  var district = CB_District.node().value;

  console.log(district);
  
  /* data route */
  const cdurl = "api/cdSummary" + "/" + district;
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
  populateDistricts();
};

init(); 









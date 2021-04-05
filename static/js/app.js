
d3.selectAll("body").on("change", buildLinePlot);

function buildLinePlot() {
  console.log("loading data...")  
  
  // Use D3 to select the dropdown menu
  var dropdownMenu = d3.select("#selYear");
  // Assign the value of the dropdown menu option to a variable
  var year = dropdownMenu.node().value;

  console.log(year);
  
  /* data route */
  const url = "api/daterequested" + "/" + year;
  d3.json(url).then(function(response) {
    /////////////////////////////////////////////////
    // Multiline Plot SR over time
    /////////////////////////////////////////////////
    console.log(year);
    const data = response;
    console.log(data);

    month = []
    count = []
    for (const [key, value] of Object.entries(data)) {
      console.log(`${key}: ${value}`);
      month.push(key);
      count.push(value);
    }
    
    countbymonth = [{
      x: month,
      y: count }];
  
    var lineplot = d3.selectAll("#line-plot").node();
  
    Plotly.newPlot(lineplot, countbymonth);
    console.log("Date loaded.")
    
  });
}

buildLinePlot();
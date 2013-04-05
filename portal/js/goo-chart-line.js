function draw_line(data, divid) {

// Set the dimensions of the canvas / graph
var	margin = {top: 30, right: 30, bottom: 30, left: 40},
	width = 300 - margin.left - margin.right,
	height = 150 - margin.top - margin.bottom;

// Parse the date / time
var formatTime = d3.time.format("%e %B");			// Format the date / time for tooltips

// Set the ranges
var	x = d3.time.scale().range([0, width]);
var	y = d3.scale.linear().range([height, 0]);

// Define the axes
var	xAxis = d3.svg.axis()
    .ticks(d3.time.months, 1)
    .tickFormat(d3.time.format("%b"))
    .scale(x)
   	.orient("bottom").ticks(5);

var	yAxis = d3.svg.axis().scale(y)
	.orient("left").ticks(3);

// Define the line
var	valueline = d3.svg.line()
	.x(function(d) { return x(d.date); })
	.y(function(d) { return y(d.value); });

// Define 'div' for tooltips
var div = d3.select(divid).append("div")	    // declare the properties for the div used for the tooltips
	.attr("class", "tooltip")				// apply the 'tooltip' class
	.style("opacity", 0);					// set the opacity to nil

// Adds the svg canvas
var	svg = d3.select(divid)
	.append("svg")
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
	.append("g")
		.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	// Scale the range of the data
	x.domain(d3.extent(data, function(d) { return d.date; }));
	y.domain([0, d3.max(data, function(d) { return d.value; })]);

	// Add the valueline path.
	svg.append("path")		
		.attr("class", "line")
		.attr("d", valueline(data));

	// draw the scatterplot
	svg.selectAll("dot")									
		.data(data)											
	.enter().append("circle")								
		.attr("r", 3)											// Made slightly larger to make recognition easier	
		.attr("cx", function(d) { return x(d.date); })		 
		.attr("cy", function(d) { return y(d.value); })			// remove semicolon	
	// Tooltip stuff after this
	    .on("mouseover", function(d) {							// when the mouse goes over a circle, do the following
            console.log(this);
			div.transition()									// declare the transition properties to bring fade-in div
				.duration(200)									// it shall take 200ms
				.style("opacity", .9);							// and go all the way to an opacity of .9
			div	.html(formatTime(d.date) + "<br/>"  + d.value)	// add the text of the tooltip as html 
				.style("left", x(d.date) + 50 + "px")			// move it in the x direction 
				.style("top", y(d.value) + "px");	// move it in the y direction
			})													// 
		.on("mouseout", function(d) {							// when the mouse leaves a circle, do the following
			div.transition()									// declare the transition properties to fade-out the div
				.duration(500)									// it shall take 500ms
				.style("opacity", 0);							// and go all the way to an opacity of nil
		});														// finis

	// Add the X Axis
	svg.append("g")	
		.attr("class", "x axis")
		.attr("transform", "translate(0," + height + ")")
		.call(xAxis);

	// Add the Y Axis
	svg.append("g")	
		.attr("class", "y axis")
		.call(yAxis);

}

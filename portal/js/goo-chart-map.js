function draw_map(map, divid) {


var width = 1024,
    height = 500,
    centered;

var projection = d3.geo.equirectangular()
    .scale(width)
    .translate([0, 0]);

var path = d3.geo.path()
    .projection(projection);

 var color = d3.scale.linear()
    .domain([2, 3, 5, 13, 20, 25])
    .range(["#f2f0f7", "#dadaeb", "#bcbddc", "#9e9ac8", "#756bb1", "#54278f"]);

var svg = d3.select(divid).append("svg")
    .attr("width", width)
    .attr("height", height);

svg.append("rect")
    .attr("class", "background")
    .attr("width", width)
    .attr("height", height)

var g = svg.append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")
    .append("g")
    .attr("id", "states");


d3.json('json/world.json', function(collection) {
    g.selectAll('path')
        .data(collection.features)
        .enter().append('path')
        .attr('d', d3.geo.path().projection(projection))
        .attr('id', function(d){return d.properties.name.replace(/\s+/g, '')})
        .style('fill', function(d){ return color(d.properties.name.length);})
        .style('stroke', 'white')
        .style('stroke-width', 1);
}); 


}

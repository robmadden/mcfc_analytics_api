var data1 = [53245, 28479, 19697, 24037, 40245],
    data2 = [200, 200, 200, 200, 200],
    data = data1;

var w = 530,
    h = 520,
    r = Math.min(w, h) / 2,
    color = d3.scale.category20(),
    donut = d3.layout.pie().sort(null),
    arc = d3.svg.arc().innerRadius(r - 260).outerRadius(r - 20);

var svg = d3.select("div").append("svg:svg")
    .attr("width", w)
    .attr("height", h)
    .append("svg:g")
    .attr("transform", "translate(" + w / 2 + "," + h / 2 + ")");

var arcs = svg.selectAll("path")
    .data(donut(data))
    .enter().append("svg:path")
    .attr("fill", function(d, i) { return color(i); })
    .attr("d", arc)
    .each(function(d) { this._current = d; });

d3.select(window).on("click", function() {
  data = data === data1 ? data2 : data1; // swap the data
  arcs = arcs.data(donut(data)); // recompute the angles and rebind the data
  arcs.transition().duration(750).attrTween("d", arcTween); // redraw the arcs
});

// Store the currently-displayed angles in this._current.
// Then, interpolate from this._current to the new angles.
function arcTween(a) {
  var i = d3.interpolate(this._current, a);
  this._current = i(0);
  return function(t) {
    return arc(i(t));
  };
}
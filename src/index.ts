import * as am4core from "@amcharts/amcharts4/core";
import * as am4maps from "@amcharts/amcharts4/maps";
import am4geodata_indiaHigh from "@amcharts/amcharts4-geodata/indiaHigh";

// // Create High detail map instance
let chart = am4core.create("chartdiv", am4maps.MapChart);

// Set map definition
chart.geodata = am4geodata_indiaHigh;

// Set projection
chart.projection = new am4maps.projections.Miller();
chart.align = "center";

// Create map polygon series
let polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());

// Make map load polygon (like country names) data from GeoJSON
polygonSeries.useGeodata = true;

// Configure series
// Zooming map objects
let polygonTemplate = polygonSeries.mapPolygons.template;
polygonTemplate.events.on("hit", function (ev) {
  chart.zoomToMapObject(ev.target);
});
polygonTemplate.tooltipText = "{name}";
polygonTemplate.fill = am4core.color("#74B266");

// Create hover state and set alternative fill color
let hs = polygonTemplate.states.create("hover");
hs.properties.fill = am4core.color("#367B25");

// Create a chart container to hold the chart label
let label = chart.chartContainer.createChild(am4core.Label);
label.text = "indiaHigh";
label.align = "center";

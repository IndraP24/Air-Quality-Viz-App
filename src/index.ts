import * as am4core from "@amcharts/amcharts4/core";
import * as am4maps from "@amcharts/amcharts4/maps";
import am4geodata_indiaHigh from "@amcharts/amcharts4-geodata/indiaHigh";

// High detail map
var chart = am4core.create("chartdiv", am4maps.MapChart);
chart.geodata = am4geodata_indiaHigh;
chart.projection = new am4maps.projections.Miller();
chart.align = "center";

var polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());
polygonSeries.useGeodata = true;
polygonSeries.mapPolygons.template.events.on("hit", function (ev) {
    chart.zoomToMapObject(ev.target);
});

var label = chart.chartContainer.createChild(am4core.Label);
label.text = "indiaHigh";
import * as am4core from "@amcharts/amcharts4/core";
import * as am4maps from "@amcharts/amcharts4/maps";
import am4geodata_IndiaHigh from "@amcharts/amcharts4-geodata/worldIndiaHigh";
import am4geodata_franceLow from "@amcharts/amcharts4-geodata/franceLow";
import am4geodata_franceHigh from "@amcharts/amcharts4-geodata/franceHigh";

// Low-detail map
var chart = am4core.create("chartdiv", am4maps.MapChart);
chart.geodata = am4geodata_franceLow;
chart.projection = new am4maps.projections.Miller();
var polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());
polygonSeries.useGeodata = true;
polygonSeries.mapPolygons.template.events.on("hit", function (ev) {
    chart.zoomToMapObject(ev.target);
});
var label = chart.chartContainer.createChild(am4core.Label);
label.text = "franceLow";

// High detail map
var chart2 = am4core.create("chartdiv2", am4maps.MapChart);
chart2.geodata = am4geodata_franceHigh;
chart2.projection = new am4maps.projections.Miller();
var polygonSeries = chart2.series.push(new am4maps.MapPolygonSeries());
polygonSeries.useGeodata = true;
polygonSeries.mapPolygons.template.events.on("hit", function (ev) {
    chart2.zoomToMapObject(ev.target);
});
var label2 = chart2.chartContainer.createChild(am4core.Label);
label2.text = "franceHigh";
## Hydrometric Discharge in the Yukon Territory

### Stations in the Yukon Territory

```js
const stations = FileAttachment("data/stations.json").json()
```

```js
import * as L from "npm:leaflet";
const div = display(document.createElement("div"));
div.style = "height: 800px;";
const map = L.map(div)
  .setView([66.748, -137.508], 5);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
})
  .addTo(map);

stations.forEach(function(location) {
    var marker = L.marker([location.LATITUDE, location.LONGITUDE]).addTo(map);
    marker.bindPopup(location.STATION_NAME); 
});
```

### Discharge Summary

```js
const discharge = FileAttachment("data/discharge.csv").csv({typed: true});
```

```js
const x = view(Inputs.range([0, 500], {step: 50, value: 0, label: "Discharge Threshold (m³/s)"}));
```

```js
function dischargePlot(data, discharge_threshold) {
    return Plot.plot({
  title: "Yukon Hydrometric Stations",
  marginLeft: 400, 
  marks: [
    Plot.barX(data, {
        filter: d => d.discharge >= discharge_threshold,
        x: "discharge", 
        y: "name", 
        fill: "name", 
        tip: true
        }),
    Plot.ruleX([0])
  ],
  y: {label: ""},
  x: {label: "Discharge (m³/s)"},
  color: {label: "Station"},
})
}
```

<div class="grid grid-cols-1">
  <div class="card">${dischargePlot(discharge, x)}
  </div>
</div>



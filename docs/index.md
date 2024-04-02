## Hydrometric Discharge in the Yukon Territory

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

$(document).ready(function () {
    const countriesListEl = $(".countries-list");
    let currentSelectedCountriesKeys = [];

    const width = 800, height = 400;
    const svg = d3.select("#map-container .map-wrapper svg").attr("width", width).attr("height", height);
    const projection = d3.geoMercator().scale(280).translate([width / 2 - 300, height / 2 + 200]);
    const path = d3.geoPath().projection(projection);
    const geoUrl = "/static/assets/js/custom.geo.json";


    const jsConfigDataEl = $("#js-config-data");
    const countryZones = JSON.parse(jsConfigDataEl.find("#zones")[0].textContent);
    const countryZonesPath = JSON.parse(jsConfigDataEl.find("#zonesPath")[0].textContent);
    const selectedCountriesKeys = countryZones.map(function (item) {
        return item.IDENTIFIER_FIELD;
    });

    d3.json(geoUrl).then(data => {
        const selectedCountriesProps = [];
        data.features.forEach(d => {
            if (selectedCountriesKeys.includes(d.properties.adm0_a3)) {
                selectedCountriesProps.push(d.properties);
            }
        });

        selectedCountriesProps.forEach(d => {
            countriesListEl.append(`<li class="list-group-item" data-country-target-key="${d.adm0_a3}" >${d.name}</li>`);
        });

        svg.selectAll(".region")
            .data(data.features)
            .enter().append("path")
            .attr("class", d => selectedCountriesKeys.includes(d.properties.adm0_a3) ? "region selected" : "region")
            .attr("d", path)
            .attr("data-country-key", d => d.properties.adm0_a3)
            .on("mouseover", function () {
                const el = $(this);
                const countryKey = el.data("country-key");
                currentSelectedCountriesKeys.push(countryKey);
                currentSelectedCountriesKeys.forEach(key => {
                    countriesListEl.find(`[data-country-target-key='${key}']`).addClass("highlighted");
                });
            })
            .on("mouseout", function () {
                const el = $(this);
                const countryKey = el.data("country-key");
                countriesListEl.find(`[data-country-target-key='${countryKey}']`).removeClass("highlighted");
                currentSelectedCountriesKeys = currentSelectedCountriesKeys.filter(key => key !== countryKey);
            });

        // Calculate lineIdentifiers data
        const zonesDictData = {};
        countryZones.forEach(item => {
            zonesDictData[item.IDENTIFIER_FIELD] = item;
        });

        const lineIdentifiers = countryZonesPath.map(path => ({
            fromCoords: zonesDictData[path.from]?.coords,
            toCoords: zonesDictData[path.to]?.coords
        })).filter(line => line.fromCoords && line.toCoords);

        console.log(zonesDictData, lineIdentifiers);

        // Draw lines
        svg.selectAll(".connector-line")
            .data(lineIdentifiers)
            .enter().append("line")
            .attr("class", "connector-line")
            .attr("x1", d => projection(d.fromCoords)[0])
            .attr("y1", d => projection(d.fromCoords)[1])
            .attr("x2", d => projection(d.toCoords)[0])
            .attr("y2", d => projection(d.toCoords)[1])
            .attr("stroke-width", 2);
    });

    $(document).on("mouseover", ".countries-list > li", function () {
        const el = $(this);
        const countryKey = el.data("country-target-key");
        $(".region[data-country-key='" + countryKey + "']").addClass("highlighted");
    });
    $(document).on("mouseout", ".countries-list > li", function () {
        const el = $(this);
        const countryKey = el.data("country-target-key");
        $(".region[data-country-key='" + countryKey + "']").removeClass("highlighted");
    });
});

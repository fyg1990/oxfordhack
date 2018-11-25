let earthquakes;
let url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv'
let logger = document.getElementById('log');

const urlTwitter = "/get-all-records";
const promiseT = fetch(urlTwitter).then(response =>{
    return response.ok ? response.json() : Promise.reject(response.status);
});

const promiseR = fetch(url).then(function (response) {
    return response.ok ? response.text() : Promise.reject(response.status);
})

initMap = async () => {
    // Create the map.
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 4,
        center: {
            lat: 37.090,
            lng: -95.712
        },
        mapTypeId: 'terrain'
    });

    let allRecords;

    promiseT.then(response =>{
        console.log(response)
        allRecords = response.records
        console.log(allRecords)


        let heatVar=[];
        for (let i = 1; i < allRecords.length; i++) {
            let data = allRecords[i];

            //mag = parseFloat(data.mag);
            latitude = parseFloat(data.pos.coordinates[1]);
            longitude = parseFloat(data.pos.coordinates[0]);
            score = parseFloat(data.score) * 1000;

            if(score < 50){
                score = score * 10
            }
            heatVar.concat(new google.maps.LatLng(latitude, longitude));
            center ={
                lat: latitude,
                lng: longitude
            }
            var cityCircle = new google.maps.Circle({
                strokeColor: '#394aff',
                strokeOpacity: 0.8,
                strokeWeight: 2,
                fillColor: '#394aff',
                fillOpacity: 0.35,
                map: map,
                center: center,
                radius: score
            });


        }

        heatmap = new google.maps.visualization.HeatmapLayer({
          data: heatVar,
          map: map
        });
    })


    promiseR.then(function (text) {
        return d3.csvParse(text);
    }).then(function (value) {

        earthquakes = value
        earthquakes.filter(obj => parseFloat(obj.mag) > 4)

        for (var i = 1; i < 500; i++) {
            var data = earthquakes[i];

            mag = parseFloat(data.mag);
            latitude = parseFloat(data.latitude);
            longitude = parseFloat(data.longitude);
            center = {
                lat: latitude,
                lng: longitude
            };

            if (mag >= 6){
                continue;
            }

            var cityCircle = new google.maps.Circle({
                strokeColor: '#ff0000',
                strokeOpacity: 0.8,
                strokeWeight: 2,
                fillColor: '#ff0000',
                fillOpacity: 0.35,
                map: map,
                center: center,
                radius: Math.pow(10, mag)
            });

            if (cityCircle.radius > 100000) {
                // bigger than level 6
                var marker = new google.maps.Marker({
                    position: center,
                    label: data.mag
                });
                console.log(data.place)
                logger.innerHTML += data.place + '<br />';

            }
        }
    });

}
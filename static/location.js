
//gets current location
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(initialize);
    } else {
        //x.innerHTML = "Geolocation is not supported by this browser.";
    }
}

function initialize(position) {
	currentlat = position.coords.latitude;
	currentlon = position.coords.longitude;
	infowindow = new google.maps.InfoWindow();
  var latlng = new google.maps.LatLng(currentlat,currentlon);
  var mapOptions = {
    zoom: 12,
    center: latlng
  }
  mapholder = document.getElementById('map-canvas')
  mapholder.style.height = '400px';
  mapholder.style.width = '60%';
  var map = new google.maps.Map(mapholder, mapOptions);
  marker = new google.maps.Marker({position:latlng,map:map,title:"You are here!"});
 google.maps.event.addListener(marker, 'mouseover', function(i) {
		infowindow.setContent("Your Current Location");
		infowindow.open(map, this);
	});
}

function populateMap()//listedValues)
{
    var locations = [
      ['Bondi Beach', -33.890542, 151.274856, 4],
      ['Coogee Beach', -33.923036, 151.259052, 5],
      ['Cronulla Beach', -34.028249, 151.157507, 3],
      ['Manly Beach', -33.80010128657071, 151.28747820854187, 2],
      ['Maroubra Beach', -33.950198, 151.259302, 1]
    ];

    mapholder = document.getElementById('map-canvas')
  mapholder.style.height = '400px';
  mapholder.style.width = '60%';
    var map = new google.maps.Map(mapholder, {
      zoom: 10,
      center: new google.maps.LatLng(-33.92, 151.25),
      mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    var infowindow = new google.maps.InfoWindow();

    var marker, i;
     var image = "http://maps.gstatic.com/intl/en_ALL/mapfiles/dd-start.png";
    for (i = 0; i < locations.length; i++) {
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(locations[i][1], locations[i][2]),
        map: map,
          icon: image,
      });

      google.maps.event.addListener(marker, 'mouseover', (function(marker, i) {
        return function() {
          infowindow.setContent(locations[i][0]);
          infowindow.open(map, marker);
        }
      })(marker, i));
    }
}

var incrVal=0;
function createMarker(value,lat,long) {
    var keyName = Object.keys(value)[incrVal];
    incrVal++;
    //alert("in marker creating"+keyName);
    var placeLoc = new google.maps.LatLng(lat, long);
    var image = "http://maps.gstatic.com/intl/en_ALL/mapfiles/dd-start.png";
    var mapOptions = {
    zoom: 12
  }
  mapholder = document.getElementById('map-canvas')
  mapholder.style.height = '400px';
  mapholder.style.width = '60%';
  var map = new google.maps.Map(mapholder, mapOptions);
    marker = new google.maps.Marker({
        map: map,
        position: placeLoc,
        icon: image,
        content: "<p>" + "ShopName: " + value[keyName][0]+ "</p>"
    });

    var latLng = marker.getPosition(); // returns LatLng object
    map.setCenter(latLng);

    google.maps.event.addListener(marker, 'mouseover', function (i) {
        infowindow.setContent(this.content);
        infowindow.open(map, this);
    });
}

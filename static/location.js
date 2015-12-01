var map;
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
    map = new google.maps.Map(mapholder, mapOptions);
  marker = new google.maps.Marker({position:latlng,map:map,title:"You are here!"});
 google.maps.event.addListener(marker, 'mouseover', function(i) {
		infowindow.setContent("Your Current Location");
		infowindow.open(map, this);
	});
}
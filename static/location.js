
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

function populateMap(locationlist)//listedValues)
{
    splitList=locationlist.split('],');
    var loctn=[];
    for(i=0;i<splitList.length;i++)
    {
        values=splitList[i].split(',');
        firstVal=values[0].split('[')[2];
        rating=values[4].split(']')[0];
        loctn.push([firstVal,values[1],values[2],values[3],rating])
    }
    var locations=loctn;

    mapholder = document.getElementById('map-canvas')
  mapholder.style.height = '400px';
  mapholder.style.width = '100%';
    var map = new google.maps.Map(mapholder, {
      zoom: 10,
      center: new google.maps.LatLng(34.0948841, -117.7206854),
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
        content:"<p><b>"+"Name: </b>"+locations[i][0]+"<br/>"+"<b>Rating: </b>"+locations[i][4]+"</p>"
      });
    var latLng = marker.getPosition(); // returns LatLng object
    map.setCenter(latLng);
      google.maps.event.addListener(marker, 'mouseover', (function(marker, i) {
        return function() {
          infowindow.setContent(this.content);
          infowindow.open(map, marker);
        }
      })(marker, i));
    }
}

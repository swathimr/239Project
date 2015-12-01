function populateMap(locationlist)//listedValues)
{
    var val = [];
    var place = new Array();
    var splitVal = locationlist.toString().split(',');
    var j = 0;
    for (i = 0; i < splitVal.length; i++) {

        if (val.length < 6) {
            val.push(splitVal[i]);
        }
        if (val.length == 5) {
            console.log(val.length);
            tempVal=[val];
            place[j] =val.slice();
            j++;
            val.length = 0;
        }
    }

    var locations=place;

    mapholder = document.getElementById('map-canvas')
  mapholder.style.height = '400px';
  mapholder.style.width = '100%';
    var map = new google.maps.Map(mapholder, {
      zoom: 6,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    var infowindow = new google.maps.InfoWindow();
    var image = "http://maps.gstatic.com/intl/en_ALL/mapfiles/dd-start.png";
    var marker, i;

    for (i = 0; i < locations.length; i++) {
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(locations[i][1], locations[i][2]),
        map: map,
        icon:image,
        content: "<p><b>Business: </b>" + locations[i][0] + "<br/>" + "<b>Rating: </b>" + locations[i][4] + "</p>"
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
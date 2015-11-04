   var map;
    function initMap() {



    var mapOptions = { 
        mapTypeId: google.maps.MapTypeId.TERRAIN,
        center: new google.maps.LatLng(address),
        zoom: 4
     };


     var geocoder = new google.maps.Geocoder();

     var address = {{ all_classes.address }};


     geocoder.geocode({'address': address}, function(results, status) {
                                              if(status == google.maps.GeocoderStatus.OK) 
                                              {
                                                  var bounds = new google.maps.LatLngBounds();
                                                  document.write(bounds.extend(results[0].geometry.location));
                                                  map.fitBounds(bounds);
                                                  new google.maps.Marker(
                                              {
                                                 position:results[0].geometry.location,
                                                 map: map
                                               }
                                               );

                                           }

                                        }
                      );

  var map = new google.maps.Map(document.getElementById("map"), mapOptions);











     // function geocodeAddress(geocoder, resultsMap) {
     //   var address = document.getElementById('address').value;
     //   console.log("Monsters Rule!")
     //   geocoder.geocode({'address': address}, function(results, status) {
     //     if (status === google.maps.GeocoderStatus.OK) {
     //       resultsMap.setCenter(results[0].geometry.location);
     //       var marker = new google.maps.Marker({
     //         map: resultsMap,
     //         position: results[0].geometry.location
     //       });
     //     } else {
     //       alert('Geocode was not successful for the following reason: ' + status);
     //     }
     //   });
     // }



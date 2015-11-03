   var map;
    function initMap() {

        var myLatLng = {lat: 37.777937, lng: -122.4409755};

        var map = new google.maps.Map(document.getElementById('map'), {
        center: myLatLng,
        zoom: 12
      });

        var marker = new google.maps.Marker({
            position: myLatLng,
            map: map,
            title: 'Classroom Location'
        });
    }

    var geocoder;

     function initialize() {
       geocoder = new google.maps.Geocoder();
       // var latlng = new google.maps.LatLng(37.777937, -122.4409755);
       var myLatLng = {lat: 37.777937, lng: -122.4409755};
       

       console.log("Did it work?");
       console.log(myLatLng.lat);
       console.log(myLatLng.lng);
     

       var mapOptions = {
         zoom: 14,
         center: myLatLng
       }
       map = new google.maps.Map(document.getElementById("map"), mapOptions);
     }



     var kailocate;
     function codeAddress() {
      console.log("in codeAdd");
       var address = document.getElementById("address").value;
       console.log(address);
       geocoder.geocode( { 'address': address}, function(results, status) {
         if (status == google.maps.GeocoderStatus.OK) {
           map.setCenter(results[0].geometry.location);
           kailocate = results[0].geometry.location;
           console.log(kailocate);
           var marker = new google.maps.Marker({
               map: map,
               position: results[0].geometry.location
           });
         } else {
           alert("Geocode was not successful for the following reason: " + status);
         }
       });
     }
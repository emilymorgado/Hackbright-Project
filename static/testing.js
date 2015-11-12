// takes an address, geocodes it, moves the center of the map to that location and adds a map marker there.


geocoder = new google.maps.Geocoder();
geocoder.geocode({ 'address': address }, function(results, status) {
  if (status == google.maps.GeocoderStatus.OK) {
    map.setCenter(results[0].geometry.location);
    var marker = new google.maps.Marker({
    map: map,
    position: results[0].geometry.location
  });






function getMonster(evt){
    event.preventDefault();

    console.log("getMonster worked!");
    var inputs = {
        "class-info" : $("#monster").html()
    }

    $.get("/testing.json", inputs, map)
}

function map(data) {
    console.log("really sent this time");
    console.log(data);
}

window.addEventListener('load', getMonster)
    console.log("addEventListener sent!");



// takes an address, geocodes it, moves the center of the map to that location and adds a map marker there.




// console.log("What's up?")
// function getMonster(evt){
//     event.preventDefault();

//     console.log("getMonster worked!");
//     var inputs = {
//         "class-info" : $("#monster").html()
//     }

//     $.get("/testing.json", address, map)
// }

// function map(address) {
//     console.log("really sent this time");
//     console.log(address);

// var geocoder;
// var map;
// var address = address;
// console.log(address)

// function initialize() {
//     geocoder = new google.maps.Geocoder();
//     geocoder.geocode({ 'address': address }, function(results, status) {
//       if (status == google.maps.GeocoderStatus.OK) {
//         map.setCenter(results[0].geometry.location);
//         var marker = new google.maps.Marker({
//         map: map,
//         position: results[0].geometry.location
//       });
// }

// window.addEventListener('load', getMonster)
//     console.log("addEventListener sent!");
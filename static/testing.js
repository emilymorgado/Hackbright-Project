
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

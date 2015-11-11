
function getMonster(evt){
    event.preventDefault();

    console.log("getMonster worked!");
    var inputs = {
        "class-info" : $("monster").html()
    }

    $.get("/testing.json", inputs, map)
}

window.addEventListener('load', getMonster)
    console.log("addEventListener sent!");

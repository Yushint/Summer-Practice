let switchMode = document.getElementById("switchMode");

switchMode.onclick = function(){
    let theme = document.getElementById("theme");
    if (theme.getAttribute("href") == "../static/css/administratorlight.css"){
        theme.href = "../static/css/administratordark.css";
    } else{
        theme.href = "../static/css/administratorlight.css";
    }
}
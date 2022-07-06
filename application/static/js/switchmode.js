let switchMode = document.getElementById("switchMode");

switchMode.onclick = function(){
    let theme = document.getElementById("theme");
    if (theme.getAttribute("href") == "../static/css/home-light-mode.css"){
        theme.href = "../static/css/home-dark-mode.css";
    } else{
        theme.href = "../static/css/home-light-mode.css";
    }
}
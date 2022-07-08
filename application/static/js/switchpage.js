let switchMode = document.getElementById("switchMode");

switchMode.onclick = function(){
    let theme = document.getElementById("theme");
    if (theme.getAttribute("href") == "../static/css/pagestyle-light.css"){
        theme.href = "../static/css/pagestyle-dark.css";
    } else{
        theme.href = "../static/css/pagestyle-light.css";
    }
}
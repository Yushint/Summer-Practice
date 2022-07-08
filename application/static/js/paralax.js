var w = window.screen.availWidth;
if(w > 1000){
    let imga = document.querySelector('.idonnow1')
    window.addEventListener('mousemove', function(e) {
        let x = e.clientX / window.innerWidth;
        let y = e.clientY / window.innerHeight;
        imga.style.transform = 'translate(+' + x * 15 + 'px, +' + y * 15 + 'px)';
    });
};


var w = window.screen.availWidth;
if(w > 1000){
    let imga = document.querySelector('.idonnow2')
    window.addEventListener('mousemove', function(e) {
        let x = e.clientX / window.innerWidth;
        let y = e.clientY / window.innerHeight;
        imga.style.transform = 'translate(+' + x * 15 + 'px, +' + y * 15 + 'px)';
    });
};
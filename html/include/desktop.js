const ajax_url = "/clev3r/control";
var moving = 0;
var ip = 0;
var seq = 0;

const callCar = data => {
    $.ajax({
        type: "PoST",
        cache: false,
        dataType: 'text',
        url: ajax_url,
        data: data
    });
};


const forward = speed => {
    callCar({action: 'speed', data: speed});
    console.log(`Forward with ${speed}.`);
};

const steer = angle => {
    callCar({action: 'steer', data: angle});
    console.log(`Steer with ${angle}.`);
};

// Prevent the page from scrolling on an iphone
// http://stackoverflow.com/questions/7768269/ipad-safari-disable-scrolling-and-bounce-effect
$(document).bind(
    'touchmove',
    function(e) {
        e.preventDefault();
    }
);

$(document).ready(function() {

    $("#motor-speed").slider({
        min: 0,
        max: 100,
        step: 5,
        value: 50
    });

    $("#steering-angle").slider({
        min: 0,
        max: 40,
        step: 5,
        value: 40
    });
});

$(document).keydown( function(event) {
    if ((event.which === 87 || event.which === 38) && !event.originalEvent.repeat) {
        //UP
        console.log("UP start");
        var power = $('#motor-speed').slider("value");
        forward(power);
    } else if ((event.which === 83 || event.which === 40) && !event.originalEvent.repeat) {
        //DOWN
        console.log("DOWN start");
        var power = $('#motor-speed').slider("value");
        forward(-power);
    } else if ((event.which === 65 || event.which === 37) && !event.originalEvent.repeat) {
        //LEFT
        console.log('ArrowLeft down');
        var angle = $('#steering-angle').slider("value");
        steer(angle);
    } else if ((event.which === 68 || event.which === 39) && !event.originalEvent.repeat) {
        //RIGHT
        console.log('ArrowLeft down');
        var angle = $('#steering-angle').slider("value");
        steer(-angle);
    }
});

$(document).keyup( function(event) {
    if ((event.which === 87 || event.which === 38) && !event.originalEvent.repeat) {
        //UP
        console.log("UP stop");
        forward(0);
    } else if ((event.which === 83 || event.which === 40) && !event.originalEvent.repeat) {
        //DOWN
        console.log("DOWN stop");
        forward(0);
    } else if ((event.which === 65 || event.which === 37) && !event.originalEvent.repeat) {
        //LEFT
        console.log('ArrowLeft up');
        steer(0);
    } else if ((event.which === 68 || event.which === 39) && !event.originalEvent.repeat) {
        //RIGHT
        console.log('ArrowRight up');
        steer(0);
    }
});
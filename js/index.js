var interval
var path1 = "draw/line1/"
var path2 = "draw/line2/"
var path3 = "draw/line3/"

var time = 20
var current_number = 0

var totalSecs = 0

function startSlideShow1() {
	interval = setInterval(setImage1, time);
}

function startSlideShow1() {
	interval = setInterval(setImage2, time);
}

function startSlideShow3() {
	interval = setInterval(setImage3, time);
}

function stopSlideShow() {
	clearInterval(interval);
	resetTime();
	totalSecs = 0;
	document.getElementById("slides").setAttribute("src", "time.png");
}

function setImage1() {
	if (current_number >= 2204) {
		stopSlideShow()
		current_number = 0
		return
	}
	document.getElementById("slides").setAttribute("src", "draw/line1/draw"+(current_number)+".jpg")
	totalSecs = totalSecs+0.3;
	setTime()
	current_number++
}

function setImage2() {
	if (current_number >= 2204) {
		stopSlideShow()
		current_number = 0
		return
	}
	document.getElementById("slides").setAttribute("src", "draw/line2/draw"+(current_number)+".jpg")
	totalSecs = totalSecs+0.3;
	setTime()
	current_number++
}


function setImage3() {
	if (current_number >= 1534) {
		stopSlideShow()
		current_number = 0
		return
	}
	totalSecs = totalSecs+0.3;
	setTime()
	document.getElementById("slides").setAttribute("src", "draw/line3/draw"+(current_number)+".jpg")
	current_number++
}


var minutesLabel = document.getElementById("minutes");
var secondsLabel = document.getElementById("seconds");
var totalSeconds = 0;

function resetTime() {
  totalSeconds = 0;
  secondsLabel.innerHTML = pad(totalSeconds % 60);
  minutesLabel.innerHTML = pad(parseInt(totalSeconds / 60));
}

function setTime() {
  totalSeconds = Math.floor(totalSecs);
  secondsLabel.innerHTML = pad(totalSeconds % 60);
  minutesLabel.innerHTML = pad(parseInt(totalSeconds / 60));
}

function pad(val) {
  var valString = val + "";
  if (valString.length < 2) {
    return "0" + valString;
  } else {
    return valString;
  }
}


var estimatedWait = {
  x: [1, 2, 3, 4],
  y: [10, 15, 13, 17],
  mode: 'lines+markers'
};

var data = [estimatedWait];

var layout1 = {
    title: 'Estimated Wait Time',
    line: {
        dash: 'dot',
        width: 0.5
    },
    xaxis: {
        title: 'Time elapsed',
    },
    yaxis: {
        title: 'Wait Time in minutes',
    }
};
var layout2 = {
    title: 'Estimated Wait Time',
    line: {
        dash: 'dot',
        width: 0.5
    },
    xaxis: {
        title: 'Time elapsed',
    },
    yaxis: {
        title: 'Wait Time in minutes',
    }
};
var layout3 = {
    title: 'Estimated Wait Time',
    line: {
        dash: 'dot',
        width: 0.5
    },
    xaxis: {
        title: 'Time elapsed',
    },
    yaxis: {
        title: 'Wait Time in minutes',
    }
};

Plotly.newPlot('ewt', data, layout1);
Plotly.newPlot('nump', data, layout);
Plotly.newPlot('vel', data, layout);
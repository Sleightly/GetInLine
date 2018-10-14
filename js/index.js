var interval
var path1 = "draw/line1/"
var path2 = "draw/line2/"
var path3 = "draw/line3/"

var max_3 = 20
var current_number = 0

function startSlideShow3() {
	interval = setInterval(setImage3, max_3);
}

function stopSlideShow() {
	clearInterval(interval);
	document.getElementById("slides").setAttribute("src", "time.png")
}

function setImage3() {
	if (current_number >= 1534) {
		stopSlideShow()
		current_number = 0
		return
	}
	document.getElementById("slides").setAttribute("src", "draw/line3/draw"+(current_number)+".jpg")
	current_number++
}



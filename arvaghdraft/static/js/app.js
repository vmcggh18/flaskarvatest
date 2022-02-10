var slideIndex = 1;
var myTimer;
// initialise myTimer and slideIndex
window.addEventListener("load", function(){
    showSlides(slideIndex);
    myTimer = setInterval(function() {plusSlides(1)}, 3000);
    var slideshowContainer = document.getElementsByClassName('slideContainer')[0];
    slideshowContainer.addEventListener('mouseenter', pause)
    slideshowContainer.addEventListener('mouseleave', resume)
})

// move slides manually with prev and next buttons
function plusSlides(n) {
  clearInterval(myTimer);
  if (n < 0) {
      showSlides(slideIndex -= 1)
  } else {
      showSlides(slideIndex += 1)
  }
  if (n === -1) {
      myTimer = setInterval(function() {plusSlides (n + 2)}, 3000);
  } else {
      myTimer = setInterval(function() {plusSlides (n + 1)}, 3000);
  }
}
//Controls the current slide and resets interval if needed
function currentSlide(n) {
  clearInterval(myTimer);
  myTimer = setInterval(function() {plusSlides(n + 1)}, 3000);
  showSlides(slideIndex = n);
}
// note: dots in this case are thumbnails
function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("slide");
  var dots = document.getElementsByClassName("thumbImage");
  var captionText = document.getElementById("caption");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
  captionText.innerHTML = dots[slideIndex-1].alt;
}
pause = () => {
  clearInterval(myTimer);
}
resume = () =>{
  clearInterval(myTimer);
  myTimer = setInterval(function(){plusSlides(slideIndex)}, 3000);
}


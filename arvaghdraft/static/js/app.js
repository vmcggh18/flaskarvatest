// move slides manually
function setSlide(number){
   clearSelected();
   currentSlide(number);
   document.querySelectorAll('.thumbImage')[number-1].style.borderBottom = "6px solid #FFA836";
}
function clearSelected(){
   Array.from(document.querySelectorAll('.thumbImage')).forEach(item=>item.style.borderBottom="");
}
document.querySelector(".prevBtn").addEventListener("click", () => {
   changeSlides(-1);
});
document.querySelector(".nextBtn").addEventListener("click", () => {
   changeSlides(1);
});
var slideIndex = 1;
showSlides(slideIndex);
function changeSlides(n) {
   showSlides((slideIndex += n));
}
function currentSlide(n) {
   showSlides((slideIndex = n));
}
function showSlides(n) {
   var i;
   var slides = document.getElementsByClassName("slide");
   if (n > slides.length) {
      slideIndex = 1;
   }
   if (n < 1) {
      slideIndex = slides.length;
   }
   Array.from(slides).forEach(item => (item.style.display = "none"));
   slides[slideIndex - 1].style.display = "block";
}
//  move slides automatically
var slideIndex = 0;
carousel();

function carousel() {
var j;
var x = document.getElementsByClassName("slide");
for (j = 0; j < x.length; j++) {
   x[j].style.display = "none";
}
slideIndex++;
if (slideIndex > x.length) {slideIndex = 1}
x[slideIndex-1].style.display = "block";
setTimeout(carousel, 3000); // Change image every 2 seconds
}


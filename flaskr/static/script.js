window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  // if (document.body.scrollTop > 80 || document.documentElement.scrollTop > 80) {
    
  //   document.getElementById("navbar").style.background = "rgba(0,0,0,1.0)";

  // } else if() {
    
  //   document.getElementById("navbar").style.background = "rgba(0,0,0,0.4)";
  // }
  if(window.scrollY>620)
  {
  	document.getElementById("navbar").style.background = "rgba(191, 191, 191,1)";
  	document.getElementById("navbar").style.color = "rgb(0,0,0)";
  }
  else if(window.scrollY<=420)
  {
  	document.getElementById("navbar").style.background = "rgba(0,0,0,0.4)";
  	document.getElementById("navbar").style.color = "white";

  }
}
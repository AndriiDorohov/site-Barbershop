const toTopButton = document.getElementById("to-top-btn");

toTopButton.addEventListener("click", function () {
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
});


window.addEventListener('scroll', function() {
    var button = document.querySelector('.to-top-btn');
    var windowHeight = window.innerHeight;
    var scrollY = window.scrollY || window.pageYOffset;

    if (scrollY > windowHeight  / 2) {
        button.style.display = 'block';
    } else {
        button.style.display = 'none';
    }
});

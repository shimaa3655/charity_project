document.addEventListener("DOMContentLoaded", function() {
    var imgElement = document.getElementById('backgroundImage');
    var images = imgElement.dataset.images.split(',');

    var currentIndex = 0;

    setInterval(function() {
        currentIndex = (currentIndex + 1) % images.length;
        imgElement.src = images[currentIndex];
    }, 3000);
});




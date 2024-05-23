document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.buttonnav').addEventListener('click', function () {
        document.getElementById('sidebar').classList.toggle('active');
    });

    var navbar = document.getElementById("navbar");
    var lastScrollTop = 0;

    function stickyNavbar() {
        var currentScroll = window.pageYOffset || document.documentElement.scrollTop;
        if (currentScroll > lastScrollTop) {
            navbar.classList.remove("sticky");
        } else {
            navbar.classList.add("sticky");
        }
        lastScrollTop = currentScroll;
    }

    window.onscroll = function() { stickyNavbar() };
});


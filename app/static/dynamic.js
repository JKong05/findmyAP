document.addEventListener("DOMContentLoaded", function() {
    var typed = new Typed('.dynamic-title', {
        strings: [
            "save <span style='color: #3B71CA;'>time</span>",
            "save <span style='color: #3B71CA;'>money</span>",
            "save <span style='color: #3B71CA;'>stress</span>",
            "findmy<span style='color: #24ace3'>A</span><span style='color: #97ca4f'>P</span>"
        ],
        typeSpeed: 150,
        backSpeed: 150,
        onComplete: function() {
            document.querySelector('.typed-cursor').style.display = 'none';
        }
    });
})

'use strict'; 
var aria = aria || {};

document.addEventListener("DOMContentLoaded", function () {

    var settingsLink = document.getElementById("settings-link");
    var netspiderLink = document.getElementById("netspider-link");
    var keywordLink = document.getElementById("keyword-link");
    var helpLink = document.getElementById("help-link");
    var resultsLink = document.getElementById("results-link")

    var boxes = document.querySelectorAll(".box");
    var bigBox = document.getElementById("big-box");
    var medBox = document.getElementById("med-box");
    var smBox = document.getElementById("small-box");
    var bigBox2 = document.getElementById("big-box-2");

    function addHoverEffect(element) {
        element.classList.add("hover-effect");

        setTimeout(function () {
            element.classList.remove("hover-effect");
        }, 1000);
    }

    settingsLink.addEventListener("click", function () {
        boxes.forEach(function (box) {
            addHoverEffect(box);
        });
    });

    netspiderLink.addEventListener("click", function () {
        addHoverEffect(bigBox);
    });

    keywordLink.addEventListener("click", function () {
        addHoverEffect(medBox);
    });

    helpLink.addEventListener("click", function () {
        addHoverEffect(smBox);
    });

    resultsLink.addEventListener("click", function () {
        addHoverEffect(bigBox2); // Assuming there's a big box 2, adjust accordingly
    });

});


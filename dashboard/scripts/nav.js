'use strict'; 
var aria = aria || {}; 

document.addEventListener("DOMContentLoaded", function () {

    var settingsLink = document.getElementById("settings-link");
    var netspiderLink = document.getElementById("netspider-link");
    var keywordLink = document.getElementById("keyword-link");
    var HelpLink = document.getElementById("help-link");

    var boxes = document.querySelectorAll(".box");
    var bigBox = document.getElementById("big-box");
    var medBox = document.getElementById("med-box");
    var smBox = document.getElementById("small-box");

    settingsLink.addEventListener("click", function () {
        // Trigger hover effect on the three boxes
        boxes.forEach(function (box) {
            box.classList.add("hover-effect");
        });

        setTimeout(function () {
            boxes.forEach(function (box) {
                box.classList.remove("hover-effect");
            });
        }, 1000);
    });

    netspiderLink.addEventListener("click", function () {
        // Trigger hover effect on the big box
        bigBox.classList.add("hover-effect");

        setTimeout(function () {
            bigBox.classList.remove("hover-effect");
        }, 1000);
    });

    keywordLink.addEventListener("click", function () {
        // Trigger hover effect on the med box
        medBox.classList.add("hover-effect");

        setTimeout(function () {
            medBox.classList.remove("hover-effect");
        }, 1000);
    });

    HelpLink.addEventListener("click", function () {
        // Trigger hover effect on the small box
        smBox.classList.add("hover-effect");

         setTimeout(function () {
            smBox.classList.remove("hover-effect");
         }, 1000);
    });

});

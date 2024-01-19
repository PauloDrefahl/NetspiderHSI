document.addEventListener("DOMContentLoaded", function () {
    var settingsLink = document.getElementById("settings-link");
    var netspiderLink = document.getElementById("netspider-link");
    var boxes = document.querySelectorAll(".box");
    var bigBox = document.getElementById("big-box");

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
});

document.addEventListener("DOMContentLoaded", function () {
    const fileInputs = document.querySelectorAll('.file-input');

    fileInputs.forEach(input => {
        input.addEventListener('change', function () {
            if (this.files.length > 0) {
                this.classList.add('file-selected');
            } else {
                this.classList.remove('file-selected');
            }
        });
    });
});



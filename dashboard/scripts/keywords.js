document.addEventListener("DOMContentLoaded", function() {
    // Get reference to the select element and the button
    var itemList = document.getElementById("itemList");
    var selectAllBtn = document.getElementById("select-all-btn");

    // Add click event listener to the button
    selectAllBtn.addEventListener("click", function() {
        // Check if all options are currently selected
        var allSelected = true;
        for (var i = 0; i < itemList.options.length; i++) {
            if (!itemList.options[i].selected) {
                allSelected = false;
                break;
            }
        }

        // Toggle selection
        for (var i = 0; i < itemList.options.length; i++) {
            itemList.options[i].selected = !allSelected;
        }
    });
});

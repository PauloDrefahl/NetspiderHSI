let selectedWebsite = ""; // Declare selectedWebsite globally
let selectedLocation = ""; // Declare selectedLocation globally
let flaggedKeywords = []; // Declare flagged keywords list globally

document.addEventListener("DOMContentLoaded", function() {
    // Get reference to the select element and the button
    const itemList = document.getElementById("itemList");
    const selectAllBtn = document.getElementById("select-all-btn");

    // Add click event listener to the button
    selectAllBtn.addEventListener("click", function() {
        // Check if all options are currently selected
        let allSelected = true;
        for (let j = 0; j < itemList.options.length; j++) {
            if (itemList.options[j].style.backgroundColor === "red") {
                itemList.options[j].style.backgroundColor = ""; // Remove red background color
                unflagKeyword(itemList.options[j].textContent); // Remove keyword from flaggedKeywords array
            }
            if (!itemList.options[j].selected) {
                allSelected = false;
                break;
            }
        }

        // Toggle selection
        for (let i = 0; i < itemList.options.length; i++) {
            itemList.options[i].selected = !allSelected;
        }
    });

});


// function to change shown locations based on Website Choice
function updateDropdown() {
    let radioValue = document.querySelector('input[name="website"]:checked').value;
    selectedWebsite = radioValue; // Assign value to selectedWebsite globally
    let dropdownContent = document.querySelector('.dropdown-content');

    dropdownContent.innerHTML = ''; // Clear previous options

    if (radioValue === 'Escort Alligator') {
      addOption('Dayton');
      addOption('Fort Lauderdale');
      addOption('Fort Myers');
      addOption('Gainesville');
      addOption('Jacksonville');
      addOption('Keys');
      addOption('Miami');
      addOption('Ocala');
      addOption('Okaloosa');
      addOption('Orlando');
      addOption('Palm Bay');
      addOption('Panama City');
      addOption('Pensacola');
      addOption('Bradenton');
      addOption('Space Coast');
      addOption('St. Augustine');
      addOption('Tallahassee');
      addOption('Tampa');
      addOption('Treasure Coast');
      addOption('West Palm Beach');
      addOption('Jacksonville');
  } else if (radioValue === 'Mega Personals') {
      addOption('Dayton');
      addOption('Fort Lauderdale');
      addOption('Fort Myers');
      addOption('Gainesville');
      addOption('Jacksonville');
      addOption('Keys');
      addOption('Miami');
      addOption('Ocala');
      addOption('Okaloosa');
      addOption('Orlando');
      addOption('Palm Bay');
      addOption('Panama City');
      addOption('Pensacola');
      addOption('Bradenton');
      addOption('Space Coast');
      addOption('St. Augustine');
      addOption('Tallahassee');
      addOption('Tampa');
      addOption('Treasure Coast');
      addOption('West Palm Beach');
      addOption('Jacksonville');
  } else if (radioValue === 'Skip The Games') {
      addOption('Bonita Springs');
      addOption('Bradenton');
      addOption('Cape Coral');
      addOption('Fort Myers');
      addOption('Ocala');
      addOption('Okaloosa');
      addOption('Orlando');
      addOption('Palm Bay');
      addOption('Gainesville');
      addOption('Jacksonville');
      addOption('Keys');
      addOption('Miami');
      addOption('Naples');
      addOption('Space Coast');
      addOption('St. Augustine');
      addOption('Tallahassee');
      addOption('Tampa');
      addOption('Sarasota');
      addOption('West Palm Beach');
      addOption('Venice');
  } else if(radioValue === 'Yes Back Page'){
      addOption('Florida');
      addOption('Broward');
      addOption('Daytona Beach');
      addOption('Florida Keys');
      addOption('Ft Myers-SW Florida');
      addOption('Gainesville');
      addOption('Jacksonville');
      addOption('Lakeland');
      addOption('Miami');
      addOption('Ocala');
      addOption('Orlando');
      addOption('Palm Beach');
      addOption('Panama City');
      addOption('Pensacola-Panhandle');
      addOption('Sarasota-Bradenton');
      addOption('Space Coast');
      addOption('St Augustine');
      addOption('Tallahassee');
      addOption('Tampa Bay Area');
      addOption('Treasure Coast');
      addOption('West Palm Beach');
  } else if(radioValue === 'Eros'){
      addOption('Miami');
      addOption('Naples');
      addOption('North Florida');
      addOption('Orlando');
      addOption('Tampa');
  }
}
// Actually displays dropdown
function addOption(location) {
    let option = document.createElement('a');
    option.href = '#';
    option.textContent = location;
    option.classList.add('dropdown-item');
    option.addEventListener('click', function() {
        selectedLocation = location; // Assign value to selectedLocation globally

        // Update the label text to display the selected city
        let selectLocationLabel = document.querySelector('.dropdown-item');
        selectLocationLabel.textContent = selectedLocation;

        // Remove "selected" class from all options
        let allOptions = document.querySelectorAll('.dropdown-item');
        allOptions.forEach(function(opt) {
            opt.classList.remove('selected');
        });

        // Add "selected" class to the clicked option
        option.classList.add('selected');
    });
    document.querySelector('.dropdown-content').appendChild(option);


}

document.addEventListener('DOMContentLoaded', function () {
    let selectLocationLink = document.querySelector('.dropdown-item');
    selectLocationLink.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent the default behavior
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const itemList = document.getElementById("itemList");

    // Add click event listener to list items
    itemList.addEventListener("click", function(event) {
        const selectedItem = event.target;
        if (selectedItem.tagName === "OPTION") {
            selectedItem.selected = !selectedItem.selected;
            selectedItem.classList.toggle("selected");
        }
    });

    // Add double click event listener to list items
    itemList.addEventListener("dblclick", function(event) {
        event.preventDefault(); // Prevent default double-click behavior
        const flaggedItem = event.target;
        if (flaggedItem.tagName === "OPTION") {
            flaggedItem.classList.toggle("flagged");
        }
    });

});



function flagKeyword(keyword) {
    keyword = keyword.trim(); // Remove leading and trailing whitespace characters
    if (!flaggedKeywords.includes(keyword)) {
        flaggedKeywords.push(keyword); // Add keyword to the flaggedKeywords array if not already present
    }
    console.log("Flagged Keywords:", flaggedKeywords);
}

function unflagKeyword(keyword) {
    keyword = keyword.trim(); // Remove leading and trailing whitespace characters
    const index = flaggedKeywords.indexOf(keyword);
    if (index !== -1) {
        flaggedKeywords.splice(index, 1); // Remove keyword from the flaggedKeywords array
    }
    console.log("Flagged Keywords:", flaggedKeywords);
}

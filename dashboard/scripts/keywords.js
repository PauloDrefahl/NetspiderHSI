var selectedWebsite = ""; // Declare selectedWebsite globally
var selectedLocation = ""; // Declare selectedLocation globally

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


// function to change shown locations based on Website Choice
function updateDropdown() {
    var radioValue = document.querySelector('input[name="website"]:checked').value;
    selectedWebsite = radioValue; // Assign value to selectedWebsite globally
    var dropdownContent = document.querySelector('.dropdown-content');

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
  } else if (radioValue == 'Skip The Games') {
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
  } else if(radioValue == 'Yes Back Page'){
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
    var option = document.createElement('a');
    option.href = '#';
    option.textContent = location;
    option.classList.add('dropdown-item');
    option.addEventListener('click', function() {
        selectedLocation = location; // Assign value to selectedLocation globally
        
        // Update the label text to display the selected city
        var selectLocationLabel = document.querySelector('.dropdown-item');
        selectLocationLabel.textContent = selectedLocation;

        // Remove "selected" class from all options
        var allOptions = document.querySelectorAll('.dropdown-item');
        allOptions.forEach(function(opt) {
            opt.classList.remove('selected');
        });

        // Add "selected" class to the clicked option
        option.classList.add('selected');
    });
    document.querySelector('.dropdown-content').appendChild(option);
}

document.addEventListener('DOMContentLoaded', function () {
    var selectLocationLink = document.querySelector('.dropdown-item');
    selectLocationLink.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent the default behavior
    });
});

function StartScraper() {
    startClock();
    console.log("Selected Website: ", selectedWebsite, "Selected Location: ", selectedLocation);
    
    // Clear the selectedOptions array
    selectedOptions = [];
    
    // Get all selected options from the itemList
    $("#itemList option:selected").each(function() {
        selectedOptions.push($(this).val()); // Push the value of the selected option to the array
    });
    
    // Log the selected items
    console.log("Keywords: ", selectedOptions);
}

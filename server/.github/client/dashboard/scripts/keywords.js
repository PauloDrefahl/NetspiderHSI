let selectedWebsite = ""; // Declare selectedWebsite globally
let selectedLocation = ""; // Declare selectedLocation globally
let flaggedKeywords = []; // Declare flagged keywords list globally
let selectedKeywords = []; // Declare selected keywords list globally
let selectedKeywordsInEditList = [] // Declare selected keywords in Edit list globally
let selectedKeysetEditList = "" // Declare selected keyset in Edit list globally

// function to change shown locations based on Website Choice
function updateDropdown() {
    let radioValue = document.querySelector('input[name="website"]:checked').value;
    // selectedWebsite = radioValue; // Assign value to selectedWebsite globally
    let dropdownContent = document.querySelector('.dropdown-content');

    dropdownContent.innerHTML = ''; // Clear previous options

    if (radioValue === 'Escort Alligator') {
        selectedWebsite = 'escortalligator';
        addOption('daytona');
        addOption('fort lauderdale');
        addOption('fort myers');
        addOption('gainesville');
        addOption('jacksonville');
        addOption('keys');
        addOption('miami');
        addOption('ocala');
        addOption('okaloosa');
        addOption('orlando');
        addOption('palm bay');
        addOption('panama city');
        addOption('pensacola');
        addOption('bradenton');
        addOption('space coast');
        addOption('st. augustine');
        addOption('tallahassee');
        addOption('tampa');
        addOption('treasure coast');
        addOption('west palm beach');
        addOption('jacksonville');
    } else if (radioValue === 'Mega Personals') {
        selectedWebsite = 'megapersonals';
        addOption('daytona');
        addOption('fort lauderdale');
        addOption('fort myers');
        addOption('gainesville');
        addOption('jacksonville');
        addOption('keys');
        addOption('miami');
        addOption('ocala');
        addOption('okaloosa');
        addOption('orlando');
        addOption('palm bay');
        addOption('panama city');
        addOption('pensacola');
        addOption('bradenton');
        addOption('space coast');
        addOption('st. augustine');
        addOption('tallahassee');
        addOption('tampa');
        addOption('treasure coast');
        addOption('west palm beach');
        addOption('jacksonville');
    } else if (radioValue === 'Skip The Games') {
        selectedWebsite = 'skipthegames';
        addOption('bonita springs');
        addOption('bradenton');
        addOption('cape coral');
        addOption('fort myers');
        addOption('ocala');
        addOption('okaloosa');
        addOption('orlando');
        addOption('palm bay');
        addOption('gainesville');
        addOption('jacksonville');
        addOption('keys');
        addOption('miami');
        addOption('naples');
        addOption('space coast');
        addOption('st. augustine');
        addOption('tallahassee');
        addOption('tampa');
        addOption('sarasota');
        addOption('west palm beach');
        addOption('venice');
    } else if (radioValue === 'Yes Back Page') {
        selectedWebsite = 'yesbackpage';
        addOption('florida');
        addOption('broward');
        addOption('daytona beach');
        addOption('florida keys');
        addOption('ft myers-sw florida');
        addOption('gainesville');
        addOption('jacksonville');
        addOption('lakeland');
        addOption('miami');
        addOption('ocala');
        addOption('orlando');
        addOption('palm beach');
        addOption('panama city');
        addOption('pensacola-panhandle');
        addOption('sarasota-bradenton');
        addOption('space coast');
        addOption('st augustine');
        addOption('tallahassee');
        addOption('tampa bay area');
        addOption('treasure coast');
        addOption('west palm beach');
    } else if (radioValue === 'Eros') {
        selectedWebsite = 'eros';
        addOption('miami');
        addOption('naples');
        addOption('north florida');
        addOption('orlando');
        addOption('tampa');
    }

}

// Actually displays dropdown
function addOption(location) {
    let option = document.createElement('a');
    option.href = '#';
    option.textContent = location;
    option.classList.add('dropdown-item');
    option.addEventListener('click', function () {
        selectedLocation = location; // Assign value to selectedLocation globally

        // Update the label text to display the selected city
        let selectLocationLabel = document.querySelector('.dropdown-item');
        selectLocationLabel.textContent = selectedLocation;

        // Remove "selected" class from all options
        let allOptions = document.querySelectorAll('.dropdown-item');
        allOptions.forEach(function (opt) {
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


// functions for selecting and unselecting keywords
document.addEventListener("DOMContentLoaded", function () {
    const itemList = document.getElementById("itemList");

    // Add click event listener to list items
    itemList.addEventListener("click", function (event) {
        const selectedItem = event.target;
        if (selectedItem.tagName === "OPTION") {
            selectedItem.selected = !selectedItem.selected;
            selectedItem.classList.toggle("selected");
            if (selectedItem.classList.contains("selected")) {
                selectKeyword(selectedItem.textContent)
            } else {
                unselectKeyword(selectedItem.textContent)
            }
        }
    });

    // Add double click event listener to list items
    itemList.addEventListener("dblclick", function (event) {
        event.preventDefault(); // Prevent default double-click behavior
        const flaggedItem = event.target;
        if (flaggedItem.tagName === "OPTION") {
            flaggedItem.classList.toggle("flagged");
            if (flaggedItem.classList.contains("flagged")) {
                flagKeyword(flaggedItem.textContent)
            } else {
                unflagKeyword(flaggedItem.textContent)
            }
        }
    });

});

// function for selecting all keywords and keyset keywords
document.addEventListener("DOMContentLoaded", function () {
    // Get reference to the select element and the button
    const itemList = document.getElementById("itemList");
    const selectAllBtn = document.getElementById("select-all-btn");
    const dropdownContentKeyset = document.querySelector('.dropdown-content-keyset');

    // Function to parse the text file and update the keyset

    // Add click event listener to the button
    selectAllBtn.addEventListener("click", function () {
        // Toggle selection for all options
        for (let i = 0; i < itemList.options.length; i++) {
            const option = itemList.options[i];
            option.selected = !option.selected;

            // Update styling and arrays based on selection status
            if (option.selected) {
                option.classList.add("selected"); // Apply selected styling
                selectKeyword(option.textContent); // Add keyword to selectedKeywords array
            } else {
                option.classList.remove("selected"); // Remove selected styling
                option.classList.remove('flagged'); // remove flagged styling
                unselectKeyword(option.textContent); // Remove keyword from selectedKeywords array
                unflagKeyword(option.textContent);
            }
        }
    });

    // Add event listener to the dropdown options
    dropdownContentKeyset.addEventListener("click", function (event) {
        // Check if the clicked element has the class "dropdown-item-keyset"
        if (event.target.classList.contains('dropdown-item-keyset')) {
            // Get the text content of the clicked element
            const selectedKeyset = event.target.textContent.trim();
            console.log("option selected: ", selectedKeyset)

            // Pass the selected keyset to the function
            selectKeysetKeywords(selectedKeyset);
        }
    });

});

//function for selecting keywords in key set
function selectKeysetKeywords(selectedKeyset, callback) {
    const itemList = document.getElementById("itemList");

    // Reload keysets from file and wait for completion
    window.editFile.reloadKeysetsFromFile(keywordsSetFile.path, (error, updatedData) => {
        if (error) {
            console.error('Error reloading keysets:', error);
            return;
        }

        // Get the updated keywords related to the selected keyset
        let selectedOptions = updatedData[selectedKeyset];
        console.log("updated jsonData: ", updatedData);
        console.log("selected options: ", selectedOptions);

        // Check if selectedOptions is undefined or not an array
        if (selectedOptions && Array.isArray(selectedOptions)) {
            for (let i = 0; i < itemList.options.length; i++) {
                const option = itemList.options[i];
                const keyword = option.textContent.trim();
                const isSelected = selectedOptions.includes(keyword); // Check if keyword is in selectedOptions

                if (isSelected && !option.classList.contains('selected')) {
                    option.classList.add('selected');
                    selectKeyword(keyword);
                } else if (!isSelected && option.classList.contains('selected')) {
                    option.classList.remove('selected');
                    unselectKeyword(keyword);
                }
            }
        } else {
            console.error(`Selected options for keyset "${selectedKeyset}" not found or not an array.`);
        }

        // Execute the callback function if provided
        if (callback) {
            callback();
        }
    });
}

// selected keyword is added to selectedKeywords array
function selectKeyword(keyword) {
    keyword = keyword.trim();
    if (!flaggedKeywords.includes(keyword)) {
        if (!selectedKeywords.includes(keyword)) {
            selectedKeywords.push(keyword); // Add keyword to the selectedKeywords array if not already present
        }
    }
    console.log("Selected Keywords:", selectedKeywords);
}

// remove keyword from selectedKeywords array
function unselectKeyword(keyword) {
    keyword = keyword.trim();
    if (!flaggedKeywords.includes(keyword)) {
        const index = selectedKeywords.indexOf(keyword);
        if (index !== -1) {
            selectedKeywords.splice(index, 1); // Remove keyword from the selectedKeywords array
        }
    }
    console.log("Selected Keywords:", selectedKeywords);
}

// flagged keyword is added to both selectedKeywords array and flaggedKeywords
function flagKeyword(flaggedKeyword) {
    flaggedKeyword = flaggedKeyword.trim(); // Remove leading and trailing whitespace characters
    if (!flaggedKeywords.includes(flaggedKeyword)) {
        flaggedKeywords.push(flaggedKeyword); // Add keyword to the flaggedKeywords array if not already present
        if (!selectedKeywords.includes(flaggedKeyword)) {
            selectedKeywords.push(flaggedKeyword); // Add keyword to the selectedKeywords array if not already present
        }
    }
    console.log("Flagged Keywords:", flaggedKeywords);
}

// flagged keyword is removed from both selectedKeywords array and flaggedKeywords
function unflagKeyword(flaggedKeyword) {
    flaggedKeyword = flaggedKeyword.trim(); // Remove leading and trailing whitespace characters
    const index = flaggedKeywords.indexOf(flaggedKeyword);
    if (index !== -1) {
        flaggedKeywords.splice(index, 1); // Remove keyword from the flaggedKeywords array
    }
    const selectedIndex = selectedKeywords.indexOf(flaggedKeyword);
    if (selectedIndex !== -1) {
        selectedKeywords.splice(selectedIndex, 1); // Remove keyword from the selectedKeywords array
    }
    console.log("Flagged Keywords:", flaggedKeywords);
}


// adding and removing keyword to keywords file
document.addEventListener("DOMContentLoaded", function () {
    window.editFile = undefined;
    const addKeywordButton = document.getElementById('addKeyword');
    const deleteKeywordButton = document.getElementById('deleteKeyword');
    const keywordInput = document.getElementById('addKeywordText');
    const editListItem = document.getElementById('itemListKeywords');
    const editKeysetList = document.getElementById('itemListSet');
    const listItem = document.getElementById('itemList');
    const addKeysetButton = document.getElementById('create-set');
    const deleteKeysetButton = document.getElementById('delete-set');
    const setName = document.getElementById('setname');

    editListItem.addEventListener("click", function (event) {
        const editSelectedItem = event.target;
        if (editSelectedItem.tagName === "OPTION") {
            editSelectedItem.selected = !editSelectedItem.selected;
            editSelectedItem.classList.toggle("selected");
            if (editSelectedItem.classList.contains("selected")) {
                selectKeywordEditList(editSelectedItem.textContent)
            } else {
                unselectKeywordEditList(editSelectedItem.textContent)
            }

        }

    });

    editKeysetList.addEventListener('click', function (event) {
        const selectedKeyset = event.target;
        const allKeysets = editKeysetList.querySelectorAll('option');

        // Deselect all other keysets
        allKeysets.forEach(option => {
            if (option !== selectedKeyset) {
                option.selected = false;
                option.classList.remove('selected');
            }
        });

        // Toggle selection for the clicked keyset
        selectedKeyset.selected = !selectedKeyset.selected;
        selectedKeyset.classList.toggle('selected');

        // If the keyset is selected, call the selectKeysetEditList function
        if (selectedKeyset.classList.contains('selected')) {
            selectedKeysetEditList = selectedKeyset.textContent.trim();
        } else {
            selectedKeysetEditList = '';
        }
    });


    addKeywordButton.addEventListener('click', function () {
        const keyword = keywordInput.value.trim(); // Fetch current value when button is clicked
        console.log("add keyword button clicked");
        console.log("keyword added:", keyword);
        if (keyword !== '') {
            console.log(keywordsFile)
            window.editFile.addKeywordToFile(keywordsFile.path, keyword);
            keywordInput.value = ''; // clear input

            // Create a new <option> element
            const option = document.createElement('option');
            option.textContent = keyword;

            // Append the new option to the end of the list
            itemList.appendChild(option);

            // Clone the option and append it to the edit list
            const editOption = option.cloneNode(true);
            editListItem.appendChild(editOption);
        }
    });

    deleteKeywordButton.addEventListener('click', function () {
        window.editFile.removeKeywordsFromFile(keywordsFile.path, selectedKeywordsInEditList);
        // Iterate over selected keywords to remove
        selectedKeywordsInEditList.forEach(selectedKeyword => {
            // Trim the selectedKeyword to remove leading and trailing whitespace
            const trimmedKeyword = selectedKeyword.trim();

            // Find the option element with the text content equal to the selected keyword
            const optionsToRemoveEditList = Array.from(editListItem.options).filter(option => option.textContent.trim() === trimmedKeyword);
            const optionsToRemoveList = Array.from(listItem.options).filter(option => option.textContent.trim() === trimmedKeyword);
            console.log("Searching for:", trimmedKeyword);
            console.log("Options to remove:", optionsToRemoveEditList);

            // If any options exist, remove them
            if (optionsToRemoveEditList.length > 0 && optionsToRemoveList.length > 0) {
                optionsToRemoveEditList.forEach(option => option.remove());
                optionsToRemoveList.forEach(option => option.remove());
                console.log("Options removed successfully");

                // Remove the keyword from selectedKeywords and flaggedKeywords arrays
                const selectedKeywordIndex = selectedKeywords.indexOf(trimmedKeyword);
                if (selectedKeywordIndex !== -1) {
                    selectedKeywords.splice(selectedKeywordIndex, 1);
                }

                const flaggedKeywordIndex = flaggedKeywords.indexOf(trimmedKeyword);
                if (flaggedKeywordIndex !== -1) {
                    flaggedKeywords.splice(flaggedKeywordIndex, 1);
                }
            } else {
                console.log("No options found to remove for keyword:", trimmedKeyword);
            }
        });

        // Clear the selectedKeywordsInEditList array after removal
        selectedKeywordsInEditList = [];

        // Log the updated list of keywords after removal
        console.log("Keywords removed:", selectedKeywordsInEditList);
    });

    addKeysetButton.addEventListener('click', function () {
        const setNameValue = setName.value.trim();

        if (setNameValue !== '' && selectedKeywordsInEditList.length > 0) {
            // Call the addKeyset function
            window.editFile.addKeyset(keywordsSetFile.path, selectedKeywordsInEditList, setNameValue);

            // Clear input fields
            setName.value = '';

            // Clear selected keywords in edit list
            selectedKeywordsInEditList = [];

            // Add the new keyset to the edit keyset list
            const option = document.createElement('option');
            option.textContent = setNameValue;
            option.value = setNameValue;
            editKeysetList.appendChild(option);

            // Update selectedKeysetEditList
            selectedKeysetEditList = setNameValue;

            // Add the new keyset to the dropdown menu
            const dropdownContent = document.querySelector('.dropdown-content-keyset');
            if (dropdownContent) {
                const dropdownItem = document.createElement('a');
                dropdownItem.href = '#';
                dropdownItem.classList.add('dropdown-item-keyset');
                dropdownItem.textContent = setNameValue;
                dropdownContent.appendChild(dropdownItem);

                console.log(`Keyset "${setNameValue}" added to the dropdown menu.`);
            } else {
                console.error('Dropdown content element not found.');
            }

            // Deselect all selected options in editListItem
            Array.from(editListItem.options).forEach(option => {
                option.selected = false;
                option.classList.remove('selected');
            });

            console.log(`Keyset "${setNameValue}" added to the list.`);
        } else {
            console.log('Set name and selected keywords are required.');
        }
    });

    deleteKeysetButton.addEventListener('click', function () {
        console.log("Selected keyset:", selectedKeysetEditList); // Add this line for debugging
        if (selectedKeysetEditList !== '') {
            // Call the removeKeyset function
            window.editFile.removeKeyset(keywordsSetFile.path, selectedKeysetEditList);

            // Remove the option element from the edit keyset list
            const optionsToRemove = Array.from(editKeysetList.options).filter(option => option.value === selectedKeysetEditList);
            if (optionsToRemove.length > 0) {
                optionsToRemove.forEach(option => option.remove());
                console.log(`Keyset "${selectedKeysetEditList}" removed from the list.`);
            } else {
                console.log(`Keyset "${selectedKeysetEditList}" not found in the list.`);
            }

            // Remove the keyset from the dropdown menu
            const dropdownKeysetItems = document.querySelectorAll('.dropdown-content-keyset a');
            if (dropdownKeysetItems) {
                dropdownKeysetItems.forEach(item => {
                    if (item.textContent.trim() === selectedKeysetEditList) {
                        item.remove();
                    }
                });
                console.log(`Keyset ${selectedKeysetEditList} removed from the dropdown.`);
            } else {
                console.log(`Keyset ${selectedKeysetEditList} not found in the dropdown.`);
            }

            // Clear selectedKeysetEditList after deletion
            selectedKeysetEditList = '';
        } else {
            console.log('Please select a keyset to delete.');
        }
    });


    function selectKeywordEditList(selectedKeyword) {
        selectedKeyword = selectedKeyword.trim(); // Remove leading and trailing whitespace characters
        if (!selectedKeywordsInEditList.includes(selectedKeyword)) {
            selectedKeywordsInEditList.push(selectedKeyword); // Add keyword to the flaggedKeywords array if not already present
            if (!selectedKeywordsInEditList.includes(selectedKeyword)) {
                selectedKeywordsInEditList.push(selectedKeyword); // Add keyword to the selectedKeywords array if not already present
            }
        }
        console.log("Keywords selected in Edit List:", selectedKeywordsInEditList);
    }

    function unselectKeywordEditList(selectedKeyword) {
        selectedKeyword = selectedKeyword.trim(); // Remove leading and trailing whitespace characters
        const index = selectedKeywordsInEditList.indexOf(selectedKeyword);
        if (index !== -1) {
            selectedKeywordsInEditList.splice(index, 1); // Remove keyword from the selectedKeywordsInEditList array
        }
        console.log("Keywords selected in Edit List:", selectedKeywordsInEditList);
    }

});

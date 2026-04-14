// Assuming data.json is in the same directory as your main script
// const dataPath = window.electronPath.join(window.nodePaths.__dirname, 'folders.json');
//
// let jsonData = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

document.addEventListener('DOMContentLoaded', () => {
    
    // operations for result manager
    const refresh_result_list = async () => {
        window.socket.emit('refresh_result_list');
    };

    const open_PDF = async (path) => {
        window.socket.emit('open_PDF', { pdf_path: path });
    };

    const open_ss_dir = async (path) => {
        window.socket.emit('open_ss_dir', { ss_path: path });
    };

    const open_raw_data = async (path) => {
        window.socket.emit('open_raw_data', { raw_path: path });
    };

    const open_clean_data = async (path) => {
        window.socket.emit('open_clean_data', { clean_path: path });
    };

    const open_diagram_dir = async (path) => {
        window.socket.emit('open_diagram_dir', { diagram_path: path });
    };

    // const generate_keywords = async (path) => {
    //     console.log("emitting view generate keywords event");
    //     path = selectedItems[0].textContent + "\\keywords\\Keywords.txt";
    //     const data = {
    //         gen_key_path: path
    //     };
    //
    //     window.socket.emit('', data);
    //     console.log("emitted data");
    // };

    const append_results = async (paths) => {
        window.socket.emit('start_append', paths);
    };


    // toggle multiple selection mode //
    let multipleSelectionEnabled = false; // Flag to track selection mode
    const selectedItems = []; // Store selected items

    // update button visasbility
    updateSubmitButtonVisibility();

    document.getElementById('submitButton').addEventListener('click', function () {
        // Check if multiple selection mode is enabled
        if (multipleSelectionEnabled) {
            // sending the selected items to the server
            const data = selectedItems.map(item => item.textContent)
            append_results(data).then(r => r);

            // Clear the selected items

            // Clear all selections
            selectedItems.forEach(item => {
                item.style.backgroundColor = ""; // Remove highlight
            });

            selectedItems.length = 0; // Clear the selectedItems array

        }

        // Turn off multiple selection mode
        multipleSelectionEnabled = false;

        // Optionally, update the UI to reflect the mode change
        document.getElementById('appendButton').textContent = "Append";

        // Update the button grid state to ensure it's disabled if no items are selected
        updateButtonGridState();

        // Hide the Submit button
        updateSubmitButtonVisibility();

    });

    // Add event listener to the list element //
    document.getElementById('list').addEventListener('click', function (e) {
        // Ensure the click is on a list item
        if (e.target && e.target.nodeName === 'LI') {
            toggleSelection(e.target);
        }
    });


    // Initially disable button grid buttons until an item is selected
    updateButtonGridState();

    // Handle the Append button click //
    document.getElementById('appendButton').addEventListener('click', function () {

        multipleSelectionEnabled = !multipleSelectionEnabled; // Toggle selection mode

        // update the UI to indicate the current mode

        // Update submit & cancel button visibility
        updateSubmitButtonVisibility();

        // Update the button grid state to ensure it's disabled if no items are selected
        updateButtonGridState();

    });

    document.getElementById('cancelButton').addEventListener('click', function () {

        multipleSelectionEnabled = !multipleSelectionEnabled; // Toggle selection mode

        // update the UI to indicate the current mode

        // Update submit & cancel button visibility
        updateSubmitButtonVisibility();

        // Update the button grid state to ensure it's disabled if no items are selected
        updateButtonGridState();

        // If switching to single selection mode, clear all but the last selected item
        if (!multipleSelectionEnabled && selectedItems.length > 1) {
            let lastSelectedItem = selectedItems.pop(); // Keep the last item
            selectedItems.forEach(item => item.style.backgroundColor = ""); // Remove highlight from others
            selectedItems.length = 0; // Clear the array
            selectedItems.push(lastSelectedItem); // Add back the last selected item
        }
    });

    // event listeners to buttons in the button grid

    document.getElementById('refreshListButton').addEventListener('click', function () {
        refresh_result_list().then(r => r);
    });

    document.getElementById('viewPdfButton').addEventListener('click', function () {
        let pdfPath = "\\screenshots\\" + selectedItems[0].textContent + ".pdf";
        let path = selectedItems[0].textContent + pdfPath;
        open_PDF(path).then(r => r);

    });

    document.getElementById('viewSsButton').addEventListener('click', function () {
        let ssPath = "\\screenshots";
        let path = selectedItems[0].textContent + ssPath;
        open_ss_dir(path).then(r => r);

    });

    document.getElementById('viewRawDataButton').addEventListener('click', function () {
        let rDataPath = "\\RAW-" + selectedItems[0].textContent + ".xlsx";
        let path = selectedItems[0].textContent + rDataPath;
        open_raw_data(path).then(r => r);
    });

    document.getElementById('viewCleanDataButton').addEventListener('click', function () {
        let cDataPath = "\\CLEAN-" + selectedItems[0].textContent + ".xlsx";
        let path = selectedItems[0].textContent + cDataPath;
        open_clean_data(path).then(r => r);
    });

    document.getElementById('viewDiagramButton').addEventListener('click', function () {
        let path = selectedItems[0].textContent;
        open_diagram_dir(path).then(r => r);
    });

    document.getElementById('generateKeywordsButton').addEventListener('click', function () {
        let genKeyPath = "\\keywords\\Keywords.txt";
        let path = selectedItems[0].textContent + genKeyPath;
        //logSelectedItems("Generate Keywords Requested: ", "\\keywords\\Keywords.txt");
    });

    // Function to toggle selection //
    function toggleSelection(item) {
        if (multipleSelectionEnabled) {
            const index = selectedItems.indexOf(item);
            if (index > -1) {
                selectedItems.splice(index, 1); // Remove item if already selected
                item.style.backgroundColor = ""; // Remove highlight
            } else {
                selectedItems.push(item); // Add item to selectedItems
                item.style.backgroundColor = "#50b8ff"; // Highlight selected item
            }
        } else {
            // Clear previous selection if multiple selection is not enabled
            selectedItems.forEach(selectedItem => {
                selectedItem.style.backgroundColor = ""; // Remove highlight
            });

            selectedItems.length = 0; // Clear the array
            selectedItems.push(item); // Add the newly selected item
            item.style.backgroundColor = "#50b8ff"; // Highlight selected item
        }

        // Update button grid state based on current selection
        updateButtonGridState();
    }

    function updateSubmitButtonVisibility() {
        const submitButton = document.getElementById('submitButton');
        const cancelButton = document.getElementById('cancelButton');
        const appendButton = document.getElementById('appendButton');
        if (multipleSelectionEnabled) {
            submitButton.classList.remove('hidden');
            cancelButton.classList.remove('hidden');
            appendButton.classList.add('hidden');

        }
        else {
            submitButton.classList.add('hidden');
            cancelButton.classList.add('hidden');
            appendButton.classList.remove('hidden');
        }
    }


    /*
      function logSelectedItems(actionMessage, pathExtension = "\\") {
        if (multipleSelectionEnabled && selectedItems.length > 0) {
          console.log(actionMessage + "Multiple Items Selected");
          selectedItems.forEach(item => console.log(item.textContent));
        }

        else if (selectedItems.length === 1) {;
          path = selectedItems[0].textContent + pathExtension;
          console.log(actionMessage + path);
        }

        else {
          console.log(actionMessage + "No item selected.");
        }
      }
    */
    function updateButtonGridState() {
        const buttonGridButtons = document.querySelectorAll('.button-result-ops');
        const hasSelectedItem = selectedItems.length > 0 && !multipleSelectionEnabled;
        buttonGridButtons.forEach(button => {
            button.disabled = !hasSelectedItem || multipleSelectionEnabled; // Enable buttons if there are selected items, otherwise disable
        });
        updateAppendButtonState();
    }

    function updateAppendButtonState() {
        const appendButton = document.getElementById('appendButton');
        const hasSelectedItems = selectedItems.length > 0;
        appendButton.disabled = !hasSelectedItems; // Disable if no items are selected, enable if at least one is selected
    }

    window.socket.on('result_manager_update', (data) => {
        // Result manager status update
    });

});
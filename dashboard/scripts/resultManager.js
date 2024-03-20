// Assuming data.json is in the same directory as your main script
//const dataPath = window.electronPath.join(window.nodePaths.__dirname, 'folders.json');
dataPath = "C:\\Users\\kskos\\WebstormProjects\\mergeIntegration\\folders.json"
console.log(dataPath);
//const jsonData = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

// List element is global, so it can be accessed from anywhere in the script
const listElement = document.getElementById('list');

// Function to read the JSON file and populate the list //
window.electronAPI.readJson(dataPath).then((jsonData) => {
  console.log('JSON data:', jsonData);
  let selectedItemContent = '';

  jsonData.forEach(item => {
    const listItem = document.createElement('li');
    listItem.textContent = item;
    listElement.appendChild(listItem);
      
    // Add click event listener to this list item
    listItem.addEventListener('click', function() {
        
      // Update the selectedItemContent variable with this item's content
      selectedItemContent = this.textContent;
      
      // Optionally, highlight the selected item
      // First, remove highlight from all items
      document.querySelectorAll('#list li').forEach(li => {
          li.classList.remove('selected'); // Assuming 'selected' is a class that styles the selected item
      });
      
      // Then, add the highlight class to the clicked item
      this.classList.add('selected');
      console.log(selectedItemContent); // For demonstration: log the selected item content
    });
  });
}).catch((error) => {
  console.error('Error reading JSON file:', error);
});

document.addEventListener('DOMContentLoaded', () => {
  // toggle multiple selection mode //
  let multipleSelectionEnabled = false; // Flag to track selection mode
  const selectedItems = []; // Store selected items

  const submitButton = document.getElementById('submitButton');
  if (multipleSelectionEnabled) {
      submitButton.classList.remove('hidden');
  } 
  
  else {
      submitButton.classList.add('hidden');
  }

  document.getElementById('submitButton').addEventListener('click', function() {
    // Check if multiple selection mode is enabled
    if (multipleSelectionEnabled) {
      console.log("Submitting selected items:");
      console.log(selectedItems.map(item => item.textContent)); // Log the text content of each selected item
      
      // sending the selected items to the server
      const data = selectedItems.map(item => item.textContent)
      append_results(data);

      // Clear the selected items

      // Clear all selections
      selectedItems.forEach(item => {
        item.style.backgroundColor = ""; // Remove highlight
      });
      
      selectedItems.length = 0; // Clear the selectedItems array

      console.log("Multiple selection mode is now disabled.");
      
    } 
      
    else {
      console.log("Multiple selection mode is not enabled. No action taken.");
    }

    // Turn off multiple selection mode
    multipleSelectionEnabled = false;
      
    // Optionally, update the UI to reflect the mode change
    document.getElementById('appendButton').textContent = "Append";

    // Update the button grid state to ensure it's disabled if no items are selected
    updateButtonGridState();

    // Hide the Submit button
    const submitButton = document.getElementById('submitButton');
    if (multipleSelectionEnabled) {
        submitButton.classList.remove('hidden');
    } 
    
    else {
      submitButton.classList.add('hidden');
    }

  });

  // Add event listener to the list element //
  document.getElementById('list').addEventListener('click', function(e) {
    // Ensure the click is on a list item
    if (e.target && e.target.nodeName === 'LI') {
      toggleSelection(e.target);
    }
  });


  // Initially disable button grid buttons until an item is selected
  updateButtonGridState();

  // Handle the Append button click //
  document.getElementById('appendButton').addEventListener('click', function() {
    multipleSelectionEnabled = !multipleSelectionEnabled; // Toggle selection mode
    // Optionally, update the UI to indicate the current mode
    this.textContent = multipleSelectionEnabled ? "Cancel" : "Append";
    console.log("Mode:", multipleSelectionEnabled ? "Multiple Selection" : "Single Selection");

    // Toggle the disabled state of the button grid buttons based on the mode
    const buttonGridButtons = document.querySelectorAll('#buttonGrid button');
    buttonGridButtons.forEach(button => {
        button.disabled = multipleSelectionEnabled; // Disable buttons in multiple selection mode
    });

    // Show the Submit button in multiple selection mode, hide it in single selection mode
    const submitButton = document.getElementById('submitButton');
    if (multipleSelectionEnabled) {
      submitButton.classList.remove('hidden');
    } 
    
    else {
      submitButton.classList.add('hidden');
    }

    // If switching to single selection mode, clear all but the last selected item
    if (!multipleSelectionEnabled && selectedItems.length > 1) {
      let lastSelectedItem = selectedItems.pop(); // Keep the last item
      selectedItems.forEach(item => item.style.backgroundColor = ""); // Remove highlight from others
      selectedItems.length = 0; // Clear the array
      selectedItems.push(lastSelectedItem); // Add back the last selected item
    }
  });

  // event listeners to buttons in the button grid
  document.getElementById('viewPdfButton').addEventListener('click', function () {
      console.log("clicked view pdf button");

      pdfPath = "\\screenshots\\" + selectedItems[0].textContent+".pdf";
      path = selectedItems[0].textContent + pdfPath;
      //logSelectedItems("PDF View Requested: ", pdfPath);
      console.log(path);

      open_PDF(path);

  });

  document.getElementById('viewSsButton').addEventListener('click', function () {
    console.log("clicked view ss dir button");
    
    ssPath = "\\screenshots";
    path = selectedItems[0].textContent + ssPath;
    //logSelectedItems("Screenshot Directory View Requested: ", ssPath);
    console.log(path);

    open_ss_dir(path);
    
  });

  document.getElementById('viewRawDataButton').addEventListener('click', function () {
    console.log("clicked view raw data button");

    rDataPath = "\\RAW-" + selectedItems[0].textContent + ".xlsx";
    path = selectedItems[0].textContent + rDataPath;
   // logSelectedItems("RAW Data View Requested: ","\\RAW-" + selectedItems[0].textContent);
    console.log(path);

    open_raw_data(path);
  });

  document.getElementById('viewCleanDataButton').addEventListener('click', function () {
    console.log("clicked view clean data button");
    
    cDataPath = "\\CLEAN-" + selectedItems[0].textContent + ".xlsx";
    path = selectedItems[0].textContent + cDataPath;
    //logSelectedItems("CLEAN Data View Requested: ", "\\CLEAN-" + selectedItems[0].textContent);
    console.log(path);

    open_clean_data(path);
  });

  document.getElementById('viewDiagramButton').addEventListener('click', function () {
    console.log("clicked view diagram dir button");
    diagramPath = "\\diagrams";
    path = selectedItems[0].textContent + diagramPath;
    console.log(path);

   // logSelectedItems("Diagram Directory View Requested: ", "\\diagrams");

    open_diagram_dir(path);
  });

  document.getElementById('generateKeywordsButton').addEventListener('click', function () {
    console.log("clicked generate keywords button");
    genKeyPath = "\\keywords\\Keywords.txt";
    path = selectedItems[0].textContent + genKeyPath;
    //logSelectedItems("Generate Keywords Requested: ", "\\keywords\\Keywords.txt");

      
  });

    // Function to toggle selection //
  function toggleSelection(item) {
    if (multipleSelectionEnabled) {
      const index = selectedItems.indexOf(item);
      if (index > -1) {
        selectedItems.splice(index, 1); // Remove item if already selected
        item.style.backgroundColor = ""; // Remove highlight
      } 
      
      else {
        selectedItems.push(item); // Add item to selectedItems
        item.style.backgroundColor = "lightblue"; // Highlight selected item
      }
    } 
    
    else {
      // Clear previous selection if multiple selection is not enabled
      selectedItems.forEach(selectedItem => {
        selectedItem.style.backgroundColor = ""; // Remove highlight
      });

      selectedItems.length = 0; // Clear the array
      selectedItems.push(item); // Add the newly selected item
      item.style.backgroundColor = "lightblue"; // Highlight selected item
    }

    // Update button grid state based on current selection
    updateButtonGridState();
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
    const buttonGridButtons = document.querySelectorAll('#buttonGrid button');
    const hasSelectedItem = selectedItems.length > 0 && !multipleSelectionEnabled;
    buttonGridButtons.forEach(button => {
        button.disabled = !hasSelectedItem; // Enable buttons if there are selected items, otherwise disable
    });
  }
  
  const open_PDF = async (path) => {
    console.log("emitting open_PDF event");
    
    const data = {
        pdf_path: path
    };

    socket.emit('open_PDF', data);
    console.log("emitted data");
  };

  const open_ss_dir = async (path) => {
    console.log("emitting view ss dir event");
    
    const data = {
        ss_path: path
    };

    socket.emit('open_ss_dir', data);
    console.log("emitted data");
  };

  const open_raw_data = async (path) => {
    console.log("emitting view ss dir event");      
    const data = {
        raw_path: path
    };

    socket.emit('open_raw_data', data);
    console.log("emitted data");
  };
  
  const open_clean_data = async (path) => {
    console.log("emitting view clean data event");         
    const data = {
        clean_path: path
    };

    socket.emit('open_clean_data', data);
    console.log("emitted data");
  };

  const open_diagram_dir = async (path) => {
    console.log("emitting view diagram event");           
    const data = {
        diagram_path: path
    };

    socket.emit('open_diagram_dir', data);
    console.log("emitted data");
  };

  const generate_keywords = async (path) => {
    console.log("emitting view generate keywords event");
    path = selectedItems[0].textContent + "\\keywords\\Keywords.txt";
    const data = {
        gen_key_path: path
    };

    socket.emit('', data);
    console.log("emitted data");
  };

  socket.on('result_manager_update', (data) => {
    console.log("Recieved result_manager_update event", data);
  });

  const append_results = async (paths) => {
    console.log("emitting view generate keywords event");
    
    socket.emit('start_append', paths);
    console.log("emitted data");
  };
 

});

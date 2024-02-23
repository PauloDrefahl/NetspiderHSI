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

document.getElementById('file1').addEventListener('change', function(e) {
    const file = e.target.files[0];

    if (!file) {
        return;
    }

    const reader = new FileReader();

    reader.onload = function(e) {
        const contents = e.target.result;
        const lines = contents.split('\n');
        
        const itemList = document.getElementById('itemList');
        itemList.innerHTML = ''; // Clear previous content
        
        lines.forEach(function(line) {
            const option = document.createElement('option');
            option.textContent = line;
            itemList.appendChild(option);
        });
    };

    reader.readAsText(file);
});

document.getElementById('file1').addEventListener('change', function(e) {
    const file = e.target.files[0];

    if (!file) {
        return;
    }

    const reader = new FileReader();

    reader.onload = function(e) {
        const contents = e.target.result;
        const lines = contents.split('\n');
        
        const itemList = document.getElementById('itemListKeywords');
        itemList.innerHTML = ''; // Clear previous content
        
        lines.forEach(function(line) {
            const option = document.createElement('option');
            option.textContent = line;
            itemList.appendChild(option);
        });
    };

    reader.readAsText(file);
});


document.getElementById('file2').addEventListener('change', function(e) {
    const file = e.target.files[0];

    if (!file) {
        return;
    }

    const reader = new FileReader();

    reader.onload = function(e) {
        const contents = e.target.result;
        jsonData = JSON.parse(contents); // Parse JSON data
        const keysets = Object.keys(jsonData); // Extract keys

        const itemList = document.getElementById('itemListSet');
        itemList.innerHTML = ''; // Clear previous content
        
        keysets.forEach(function(keyset) {
            const option = document.createElement('option');
            option.textContent = keyset;
            itemList.appendChild(option);
        });

        keysets.forEach(function(keyset) {
            addOptionKeyset(keyset);
        });

    };

    reader.readAsText(file);
});


function addOptionKeyset(keysets) {
    var option2 = document.createElement('a');
    option2.href = '#';
    option2.textContent = keysets;

    option2.classList.add('dropdown-item-keyset');

    option2.addEventListener('click', function() {
        var selectedKeyset = option2.textContent;
        
        // Update the label text to display the selected city
        var selectKeyset = document.querySelector('.dropdown-item-keyset');
        selectKeyset.textContent = selectedKeyset;
        selectKeywords(selectedKeyset);

        // Remove "selected" class from all options
        var allOptions = document.querySelectorAll('.dropdown-item-keyset');
        allOptions.forEach(function(opt) {
            opt.classList.remove('selected');
        });
  
        // Add "selected" class to the clicked option
        option2.classList.add('selected');
        
    });
    document.querySelector('.dropdown-content-keyset').appendChild(option2);
}


function selectKeywords(selectedKeyset) {
    selectedOptions = []; // Clear the array first
    // Get the selected keyset
    
    // Get the keywords related to the selected keyset
    selectedOptions = jsonData[selectedKeyset];

    for (var i = 0; i < itemList.options.length; i++) {
        // Check if the keyword belongs to the selected keyset
        if (selectedOptions.includes(itemList.options[i].value)) {
            itemList.options[i].selected = true;
        } else {
            itemList.options[i].selected = false;
        }
    }
}


async function selectFolder() {
    try {
        const handle = await window.showDirectoryPicker();
        console.log('Selected folder:', handle);

        // Get the name of the selected folder
        const folderName = handle.name;

        // Display the name of the selected folder
        document.getElementById('selected-folder').textContent = `Folder: ${folderName}`;
        console.log('Folder name:', path.dirname(folderName));
    } catch (error) {
        console.error('Error selecting folder:', error);
    }
}

// Event listener for button click
document.getElementById('select-folder-button').addEventListener('click', selectFolder);
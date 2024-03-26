let keywordsFile = ''
let keywordsSetFile = ''
let resultFolder = ''
window.resultManager = undefined;
window.electronAPI = undefined;

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
    keywordsFile = file

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
    keywordsFile = file

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
    keywordsSetFile = file;

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
    const option2 = document.createElement('a');
    option2.href = '#';
    option2.textContent = keysets;

    option2.classList.add('dropdown-item-keyset');

    option2.addEventListener('click', function() {
        const selectedKeyset = option2.textContent;

        // Update the label text to display the selected city
        const selectKeyset = document.querySelector('.dropdown-item-keyset');
        selectKeyset.textContent = selectedKeyset;
        // selectKeysetKeywords(selectedKeyset);

        // Remove "selected" class from all options
        const allOptions = document.querySelectorAll('.dropdown-item-keyset');
        allOptions.forEach(function(opt) {
            opt.classList.remove('selected');
        });
  
        // Add "selected" class to the clicked option
        option2.classList.add('selected');
        
    });
    document.querySelector('.dropdown-content-keyset').appendChild(option2);
}

document.addEventListener("DOMContentLoaded", function () {
    const openResultsFolderButton = document.getElementById('open-results-folder-btn');
    const resultsFolderButton = document.getElementById('folder-input-btn');
    openResultsFolderButton.addEventListener('click', function () {
        window.editFile.openResults(resultFolder);
    });

    resultsFolderButton.addEventListener('click', function () {
        window.socket.emit('set_result_dir');
    });

    window.socket.on('result_folder_selected', async (result_folder) => {
        console.log("Result Folder selected:", result_folder);
        resultFolder = result_folder;
        try {
            await window.resultManager.updateFoldersJSON(resultFolder);
            let dataPath = "folders.json";
            console.log(dataPath);
            const jsonData = await window.electronAPI.readJson(dataPath);
            if (Array.isArray(jsonData) && jsonData.length > 0) {
                console.log('JSON data:', jsonData);
                let selectedItemContent = '';

                const listElement = document.getElementById('list'); // Assuming you have an element with id 'list' for the list

                jsonData.forEach(item => {
                    const listItem = document.createElement('li');
                    listItem.textContent = item;
                    listElement.appendChild(listItem);

                    // Add click event listener to this list item
                    listItem.addEventListener('click', function () {

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
            } else {
                console.error('Error: JSON data is empty or not in expected format');
            }
        } catch (error) {
            console.error('Error processing result folder:', error);
        }
    });
});

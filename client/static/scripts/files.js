/* Original file path logic
let keywordsFile = ''
let keywordsSetFile = ''
let resultFolder = ''
let folderList = ''

window.resultManager = undefined;
window.electronAPI = undefined;

// Allows a file to be selected and deselected with an event listen that waits for an event on the front-end HTML
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

// When a file is selected, it reads the contents, putting it all within an array for the keyword selector to use.
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
    const listElement = document.getElementById('list'); // Ensure this element exists in your HTML

    openResultsFolderButton.addEventListener('click', function () {
        window.editFile.openResults(resultFolder);
    });

    resultsFolderButton.addEventListener('click', function () {
        window.socket.emit('set_result_dir');
    });

    window.socket.on('result_folder_selected', (data) => {

        if (data.error) {
            console.error('Error received:', data.error);
            listElement.innerHTML = `<li>Error: ${data.error}</li>`; // Display error in the list
            return;
        }

        if (data.file_explorer_opened) {
            console.log("File explorer opened but no directory was selected.");
            listElement.innerHTML = '<li>No directory selected.</li>';
            return;
        }

        if (data.result_dir) {
            console.log("Result Folder selected:", data.result_dir);
            resultFolder = data.result_dir; // Store the result directory globally if needed
        }

        folderList = data.folders; // This should match the key used in backend 'folders'
        console.log("Result list:", folderList);

        console.log("Result list:", folderList);
        if (Array.isArray(folderList) && folderList.length > 0) {
            console.log('Folders:', folderList);
            listElement.innerHTML = ''; // Clear previous entries

            folderList.forEach(item => {
                const listItem = document.createElement('li');
                listItem.textContent = item;

                listElement.appendChild(listItem);

                listItem.addEventListener('click', function () {
                    const previouslySelected = document.querySelector('#list li.selected');
                    if (previouslySelected) {
                        previouslySelected.classList.remove('selected');
                    }
                    this.classList.add('selected');
                    console.log("Selected Folder:", this.textContent); // For demonstration
                });
            });
        } else {
            console.error('Error: Folder list is empty or not in expected format');
            listElement.innerHTML = '<li>No folders found.</li>';
        }
    });

    window.socket.on('result_list_refreshed', (data) => {

        if (data.error) {
            console.error('Error received:', data.error);
            listElement.innerHTML = `<li>Error: ${data.error}</li>`; // Display error in the list
            return;
        }

        folderList = data.folders; // This should match the key used in backend 'folders'
        console.log("Result list:", folderList);

        console.log("Result list:", folderList);
        if (Array.isArray(folderList) && folderList.length > 0) {
            console.log('Folders:', folderList);
            listElement.innerHTML = ''; // Clear previous entries

            folderList.forEach(item => {
                const listItem = document.createElement('li');
                listItem.textContent = item;  // adding text conte
                listElement.appendChild(listItem);

                listItem.addEventListener('click', function () {
                    const previouslySelected = document.querySelector('#list li.selected');
                    if (previouslySelected) {
                        previouslySelected.classList.remove('selected');
                    }
                    this.classList.add('selected');
                    console.log("Selected Folder:", this.textContent); // For demonstration
                });
            });
        } else {
            console.error('Error: Folder list is empty or not in expected format');
            listElement.innerHTML = '<li>No folders found.</li>';
        }
    });
});
*/

let resultFolder = '';
let folderList = '';

window.resultManager = undefined;
window.electronAPI = undefined;

document.addEventListener("DOMContentLoaded", function () {
    const openResultsFolderButton = document.getElementById('open-results-folder-btn');
    const resultsFolderButton = document.getElementById('folder-input-btn');
    const listElement = document.getElementById('list');

    // Load keyword/keyset data from DB
    window.socket.emit('get_data');

    window.socket.on('data_response', function (data) {
        const keywords = data.keywords || [];
        const keysets = data.keysets || [];


        // Store for lookup
        window.dbKeysets = {};
        keysets.forEach(set => {
            window.dbKeysets[set.item_name] = set.keywords;
        });

        // Populate keyword list selections
        ['itemList', 'itemListKeywords'].forEach(id => {
            const list = document.getElementById(id);
            if (list) {
                list.innerHTML = '';
                keywords.forEach(k => {
                    const option = document.createElement('option');
                    option.textContent = k.keyword;
                    option.value = k.id;
                    list.appendChild(option);
                });
            }
        });

        // Populate keyset select
        const itemListSet = document.getElementById('itemListSet');
        if (itemListSet) {
            itemListSet.innerHTML = '';
            keysets.forEach(set => {
                const option = document.createElement('option');
                option.textContent = set.item_name;
                option.value = set.id;
                itemListSet.appendChild(option);
            });
        }

        // Populate dropdown keyset list
        const dropdownContainer = document.querySelector('.dropdown-content-keyset');
        if (dropdownContainer) {
            dropdownContainer.innerHTML = '';
            keysets.forEach(set => {
                addOptionKeyset(set.item_name);
            });
        }
    });

    // Result folder selection logic
    openResultsFolderButton.addEventListener('click', function () {
        window.editFile.openResults(resultFolder);
    });

    resultsFolderButton.addEventListener('click', function () {
        window.socket.emit('set_result_dir');
    });

    window.socket.on('result_folder_selected', (data) => {
        if (data.error) {
            listElement.innerHTML = `<li>Error: ${data.error}</li>`;
            return;
        }

        if (data.file_explorer_opened) {
            listElement.innerHTML = '<li>No directory selected.</li>';
            return;
        }

        if (data.result_dir) {
            resultFolder = data.result_dir;
        }

        folderList = data.folders;

        if (Array.isArray(folderList) && folderList.length > 0) {
            listElement.innerHTML = '';
            folderList.forEach(item => {
                const listItem = document.createElement('li');
                listItem.textContent = item;
                listElement.appendChild(listItem);

                listItem.addEventListener('click', function () {
                    const previouslySelected = document.querySelector('#list li.selected');
                    if (previouslySelected) {
                        previouslySelected.classList.remove('selected');
                    }
                    this.classList.add('selected');
                    console.log("Selected Folder:", this.textContent);
                });
            });
        } else {
            listElement.innerHTML = '<li>No folders found.</li>';
        }
    });

    window.socket.on('result_list_refreshed', (data) => {
        if (data.error) {
            listElement.innerHTML = `<li>Error: ${data.error}</li>`;
            return;
        }

        folderList = data.folders;
        if (Array.isArray(folderList) && folderList.length > 0) {
            listElement.innerHTML = '';
            folderList.forEach(item => {
                const listItem = document.createElement('li');
                listItem.textContent = item;
                listElement.appendChild(listItem);

                listItem.addEventListener('click', function () {
                    const previouslySelected = document.querySelector('#list li.selected');
                    if (previouslySelected) {
                        previouslySelected.classList.remove('selected');
                    }
                    this.classList.add('selected');
                    console.log("Selected Folder:", this.textContent);
                });
            });
        } else {
            listElement.innerHTML = '<li>No folders found.</li>';
        }
    });
});

// Dropdown creation function
function addOptionKeyset(keysetName) {
    const option2 = document.createElement('a');
    option2.href = '#';
    option2.textContent = keysetName;
    option2.classList.add('dropdown-item-keyset');

    option2.addEventListener('click', function () {
        const selectKeyset = document.querySelector('.dropdown-item-keyset');
        if (selectKeyset) {
            selectKeyset.textContent = keysetName;
        }

        document.querySelectorAll('.dropdown-item-keyset').forEach(opt => {
            opt.classList.remove('selected');
        });

        option2.classList.add('selected');
    });

    document.querySelector('.dropdown-content-keyset').appendChild(option2);
}
let keywordsFile = ''
let keywordsSetFile = ''

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
        selectKeysetKeywords(selectedKeyset);

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

  
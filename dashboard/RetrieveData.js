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
        const jsonData = JSON.parse(contents); // Parse JSON data
        const keysets = Object.keys(jsonData); // Extract keys

        const itemList = document.getElementById('itemListSet');
        itemList.innerHTML = ''; // Clear previous content
        
        keysets.forEach(function(keyset) {
            const option = document.createElement('option');
            option.textContent = keyset;
            itemList.appendChild(option);
        });
    };

    reader.readAsText(file);
});


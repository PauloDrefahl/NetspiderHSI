document.getElementById('fileInput').addEventListener('change', function(e) {
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
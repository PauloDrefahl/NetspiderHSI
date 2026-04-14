document.addEventListener('DOMContentLoaded', function() {
    const tableSelector = document.getElementById('tableSelector');
    const locationFilter = document.getElementById('locationFilter');

    document.getElementById('refreshDatabaseResults').addEventListener('click', function() {
        loadDatabaseResults(tableSelector.value);
    });

    tableSelector.addEventListener('change', function() {
        loadDatabaseResults(this.value);
    });

    locationFilter.addEventListener('change', function() {
        filterTableByLocation(this.value);
    });

    socket.on('database_results', function(response) {
        console.log('Received database results:', response);
        if (response.error) {
            console.error('Error:', response.error);
            showError(response.error);
        } else {
            updateResultsTable(response.data);
            updateLocationFilter(response.data);
        }
    });

    loadDatabaseResults('raw_escort_alligator_posts');
});

function loadDatabaseResults(tableName) {
    console.log('Requesting database results for table:', tableName);
    socket.emit('get_database_results', { tableName: tableName });
}

function updateLocationFilter(data) {
    const locationFilter = document.getElementById('locationFilter');
    const locations = new Set();

    locationFilter.innerHTML = '<option value="">All Locations</option>';

    data.forEach(row => {
        if (row.city_or_region) {
            locations.add(row.city_or_region);
        }
    });

    Array.from(locations).sort().forEach(location => {
        const option = document.createElement('option');
        option.value = location;
        option.textContent = location;
        locationFilter.appendChild(option);
    });
}

function filterTableByLocation(location) {
    const table = document.getElementById('scrape-results-table');
    const rows = table.getElementsByTagName('tr');

    for (let i = 1; i < rows.length; i++) {
        const row = rows[i];
        const locationCell = row.querySelector('td:nth-child(2)');

        if (!location || !locationCell) {
            row.style.display = '';
        } else {
            row.style.display = locationCell.textContent === location ? '' : 'none';
        }
    }
}

function showError(error) {
    const table = document.getElementById('scrape-results-table');
    table.innerHTML = `<tr><td>Error loading results: ${error}</td></tr>`;
}

function updateResultsTable(data) {
    const table = document.getElementById('scrape-results-table');
    const thead = table.querySelector('thead');
    const tbody = table.querySelector('tbody');

    thead.innerHTML = '';
    tbody.innerHTML = '';

    if (data && data.length > 0) {
        const headerRow = document.createElement('tr');
        Object.keys(data[0]).forEach(key => {
            const th = document.createElement('th');
            th.textContent = key;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);

        data.forEach(row => {
            const tr = document.createElement('tr');
            Object.values(row).forEach(value => {
                const td = document.createElement('td');
                td.textContent = value;
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });
    } else {
        tbody.innerHTML = '<tr><td colspan="100%">No results found</td></tr>';
    }
}


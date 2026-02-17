// initialize clock

let clockInterval;
let secondsElapsed = 0;
let statusText = document.getElementById('status')
let searchText = document.getElementById('scraperTextbox')
let searchMode = document.getElementById('hide_browser')
let paymentSearch = document.getElementById('payment_method')
let inclusiveSearch = document.getElementById('all_keywords')
let startButton = document.getElementById('startButton')
let stopButton = document.getElementById('stopButton')

// sets ups the clock  to display the runnning
function updateClock() {
    const hours = Math.floor(secondsElapsed / 3600).toString().padStart(2, '0');
    const minutes = Math.floor((secondsElapsed % 3600) / 60).toString().padStart(2, '0');
    const seconds = (secondsElapsed % 60).toString().padStart(2, '0');
    document.getElementById('clock').innerText = `${hours}:${minutes}:${seconds}`;
    secondsElapsed++;
}

//Starts the clock
function startClock() {
    stopClock();
    secondsElapsed = 0;
    clockInterval = setInterval(updateClock, 1000);

}

//Stops the clock
function stopClock() {
    clearInterval(clockInterval);
    clockInterval = null;
}

// Initial setup of clock - displays clock
updateClock()

//----------------------------------------------------------------

// let selectedKeywords = [];
const itemList = document.getElementById("itemList");

// Function to handle selecting all keywords
// function selectAllKeywords() {
//     selectedOptions = []; // Clear the array first
//     for (let i = 0; i < itemList.options.length; i++) {
//         itemList.options[i].selected = true;
//         selectedOptions.push(itemList.options[i].value); // Push the value of the selected option to the array
//     }
// }

//----------------------------------------------------------------

function StartScraper() {
    startClock();
    statusText.textContent = 'Status: On'
    const data = {
        website: selectedWebsite,
        city: selectedLocation,
        keywords: selectedKeywords,
        flagged_keywords: flaggedKeywords,
        search_mode: searchMode.checked,
        search_text: searchText.value,
        payment_methods_only: paymentSearch.checked,
        inclusive_search: inclusiveSearch.checked,
        path: resultFolder
    };
    window.socket.emit('start_scraper', data);
}

const StopScraper = async () => {
    stopClock()
    statusText.textContent = 'Status: Off'
    window.socket.emit('stop_scraper');
};

window.socket.on('connect', () => {});

window.socket.on('disconnect', () => {});

window.socket.on('scraper_update', (data) => {
    if (data.status === 'started') {
        // Scraper running
    } else if (data.status === 'stopped') {
        // Scraper stopped
    } else if (data.status === 'error') {
        statusText.textContent = 'Status: Error - ' + (data.error || 'Unknown');
    } else if (data.status === 'completed') {
        stopClock();
        statusText.textContent = 'Status: Off';
    }

});

const scraperStatus = async () => {
    window.socket.emit('scraper_status')
}

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
    console.log("Selected Website: ", selectedWebsite, "Selected Location: ", selectedLocation);

    // Clear the selectedKeywords array
    // selectedKeywords = [];

    // Get all selected options from the itemList
    // $("#itemList option:selected").each(function () {
    //     selectedKeywords.push($(this).val()); // Push the value of the selected option to the array
    // });

    // Log the selected items
    console.log("Keywords: ", selectedKeywords);
    statusText.textContent = 'Status: On'
    console.log("clicked start scraper button")
    const data = {
        website: selectedWebsite,
        city: selectedLocation,
        keywords: selectedKeywords.join(','),
        flagged_keywords: flaggedKeywords.join(','),
        search_mode: searchMode.checked,
        search_text: searchText.innerText,
        payment_methods_only: paymentSearch.checked,
        inclusive_search: inclusiveSearch.checked,
        path: resultFolder
    };
    window.socket.emit('start_scraper', data);
    console.log("emitted data", data);
    console.log("flagged keywords", flaggedKeywords)
    console.log("selected keywords", selectedKeywords)
}

const StopScraper = async () => {
    stopClock()
    statusText.textContent = 'Status: Off'
    console.log("stop button clicked");
    window.socket.emit('stop_scraper');
};

window.socket.on('connect', () => {
    console.log("connected");
});

window.socket.on('disconnect', () => {
    console.log("Disconnected");
});

window.socket.on('scraper_update', (data) => {
    console.log('Received scraper_update event:', data);

    // Update the UI or take any action based on the data received from the server
    if (data.status === 'started') {
        console.log('Scraper is running...');
    } else if (data.status === 'stopped') {
        console.log('Scraper completed');
    } else if (data.status === 'error') {
        console.log('Error occurred: ' + data.error);
    } else if (data.status === 'completed') {
        console.log('Scraper completed');
        stopClock();
        statusText.textContent = 'Status: Off';
    }

});

const scraperStatus = async () => {
    window.socket.emit('scraper_status')
}

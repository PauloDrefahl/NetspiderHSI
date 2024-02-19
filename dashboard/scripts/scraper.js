// initialize clock

let clockInterval;
let secondsElapsed = 0;

// sets ups the clock  to display the runnning
function updateClock() {
  const hours = Math.floor(secondsElapsed / 3600).toString().padStart(2, '0');
  const minutes = Math.floor((secondsElapsed % 3600) / 60).toString().padStart(2, '0');
  const seconds = (secondsElapsed % 60).toString().padStart(2, '0');
  const timeString = `${hours}:${minutes}:${seconds}`;
  document.getElementById('clock').innerText = timeString;
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

let selectedOptions = [];
var itemList = document.getElementById("itemList");
// Function to handle selecting all keywords
function selectAllKeywords() {
    selectedOptions = []; // Clear the array first
    for (var i = 0; i < itemList.options.length; i++) {
        itemList.options[i].selected = true;
        selectedOptions.push(itemList.options[i].value); // Push the value of the selected option to the array
    }
}

//----------------------------------------------------------------



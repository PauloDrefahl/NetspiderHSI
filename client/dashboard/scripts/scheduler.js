function saveScheduledScraper(name, duration, frequency) {
    const scraperName = name.value.trim();  // Name should be a string
    const scraperFrequency = frequency.value.trim();  // Get the selected frequency (should be a string)
    const scraperDuration = parseInt(duration.value, 10);  // Get the duration (should be a number)

    try {

        // Make sure inputs are valid
        if (!scraperName || !scraperDuration) {
            console.error('Please fill all AutoScraper fields');
            return;
        }

        const scraperData = {
            [scraperName]: {
                data: {
                    website: selectedWebsite,
                    city: selectedLocation,
                    keywords: selectedKeywords,
                    flagged_keywords: flaggedKeywords,
                    search_mode: searchMode.checked,
                    search_text: searchText.value,
                    payment_methods_only: paymentSearch.checked,
                    inclusive_search: inclusiveSearch.checked,
                    path: resultFolder
                },
                frequency: scraperFrequency,
                duration: scraperDuration,
                last_run: "none"
            }
        };
        try {
            console.log("saving scraper data ... ");
            window.scraperFile.saveScraperData('scheduled_scraper.json', scraperData);
        } catch (err) {
            console.error('Failed to save scraper data:', err);
        }
    } catch (error) {
        console.error('Error saving scheduled scraper:', error);
    }

    name.value = '';
    duration.value = '';

    // Reload the schedules
    const schedules = window.scraperFile.getSchedules();
    displaySchedules(schedules);
}

function deleteScheduledScraper(name) {
    const scraperName = name.value.trim();

    try {
        // Make sure scraperName is valid
        if (!scraperName) {
            console.error('Scraper name cannot be empty');
            return;
        }

        console.log("Deleting scraper data for:", scraperName);

        window.scraperFile.deleteScraperData('scheduled_scraper.json', { scraperName });

    } catch (error) {
        console.error('Error deleting scheduled scraper:', error);
    }

    name.value = '';

    // Reload the schedules after deletion
    const schedules = window.scraperFile.getSchedules();
    displaySchedules(schedules);
}

function preloadSchedules() {
    // Fetch the schedules from the main process
    const schedules = window.scraperFile.getSchedules();

    // Display the schedules
    displaySchedules(schedules);
}

function displaySchedules(schedules) {
    const scheduleList = document.getElementById('scheduleList'); // Get the <ul> element

    // Clear any existing content in the list
    scheduleList.innerHTML = '';

    // Iterate over the schedules and create list items
    Object.entries(schedules).forEach(([scraperName, schedule]) => {
        const listItem = document.createElement('li'); // Create a <li> element

        // Set the text content for each list item
        listItem.textContent = `Schedule: ${scraperName}, Frequency: ${schedule.frequency}, Duration: ${schedule.duration} days`;

        // Append the <li> to the <ul>
        scheduleList.appendChild(listItem);
    });
}

// Call preloadSchedules when the page is loaded
window.onload = preloadSchedules;
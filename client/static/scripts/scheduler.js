function saveScheduledScraper(name, frequency) {
    const scraperName = name.value.trim();
    const scraperFrequency = frequency.value.trim();
    const schedulerDay = document.getElementById('dayOfWeek').value;
    const schedulerTime = document.getElementById('addRunTime').value;
    const schedulerDate = document.getElementById('addRunDate').value; // YYYY-MM-DD

    try {
        if (!scraperName || !schedulerTime) {
            console.error('Please fill all AutoScraper fields');
            return;
        }

        const [hour, minute] = schedulerTime.split(':').map(x => parseInt(x, 10));

        const isWeekly = scraperFrequency === 'weekly' && !schedulerDate;
        const isDaily = scraperFrequency === 'daily' && !schedulerDate;
        const isOneTime = !!schedulerDate;

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
                daily: isDaily,
                weekly: isWeekly,
                one_time: isOneTime,
                run_date: schedulerDate || "",
                day_to_run: isWeekly ? schedulerDay : "",
                hour: hour,
                minute: minute,
                job_id: "",
                last_run: "None"
            }
        };
        try {
            console.log("saving scraper data ... ");
            window.scraperFile.saveScraperData('scheduled_scrapers.json', scraperData);
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

        window.scraperFile.deleteScraperData('scheduled_scrapers.json', { scraperName });

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
        const repeatType = schedule.one_time ? 'One-time' : schedule.weekly ? 'Weekly' : schedule.daily ? 'Daily' : schedule.frequency;
        const oneTimeText = schedule.one_time && schedule.run_date ? `, Date: ${schedule.run_date}` : '';
        const dayText = schedule.weekly ? `, Day: ${schedule.day_to_run}` : '';
        const timeText = schedule.hour !== undefined && schedule.minute !== undefined ? `, Time: ${String(schedule.hour).padStart(2,'0')}:${String(schedule.minute).padStart(2,'0')}` : '';
        listItem.textContent = `Schedule: ${scraperName}, Type: ${repeatType}${oneTimeText}${dayText}${timeText}`;

        // Append the <li> to the <ul>
        scheduleList.appendChild(listItem);
    });
}

// Call preloadSchedules when the page is loaded
window.onload = preloadSchedules;
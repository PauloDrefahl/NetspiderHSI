document.addEventListener('DOMContentLoaded', () => {
    const keywords = ['massage'];
    const flagged_keywords = ['outcall']
    const search_mode = true
    const search_text = ''
    const inclusive_search = false
    const path = 'C:\\Users\\Zach\\PycharmProjects\\NetSpiderHSI\\result'
    const cityYesBackpage = 'florida';
    const cityMegapersonals = 'daytona';
    const cityEscortalligator = 'daytona';
    const citySkipthegames = 'bonita springs'
    const cityEros = 'miami'
    const cityRubratings = 'fort myers'

    // Find the button elements by their IDs
    const startButton = document.getElementById('startButton');
    const stopButton = document.getElementById("stopButton");
    const statusText = document.getElementById('status');

    const socket = window.socket

    const startScraper = async () => {
        statusText.textContent = 'Status: On'
        console.log("clicked start scraper button")
        const data = {
            website: 'rubratings',
            city: cityRubratings,
            keywords: keywords.join(','),
            flagged_keywords: flagged_keywords.join(','),
            search_mode: search_mode,
            search_text: search_text,
            inclusive_search: inclusive_search,
            path: path
        };
        socket.emit('start_scraper', data);
        console.log("emitted data");
    };

    const stopScraper = async () => {
        statusText.textContent = 'Status: Off'
        console.log("stop button clicked");
        socket.emit('stop_scraper');
    };

    socket.on('connect', () => {
        console.log("connected");
    });
    socket.on('disconnect', () => {
        console.log('disconnect');
    });
    socket.on('scraper_update', (data) => {
        console.log('Received scraper_update event:', data);

        if (data.status === 'started') {
            console.log('Scraper is running...');
        } else if (data.status === 'completed') {
            statusText.textContent = 'Status: Off'
            console.log('Scraper completed');
        } else if (data.status === 'stopped') {
            console.log('Scraper Stopped')
        }
        // conditions based on server's 'scraper_update' data
    });

    const scraperStatus = async () => {
        socket.emit('scraper_status')
    }

    // Add click event listeners to the buttons
    startButton.addEventListener('click', async () => startScraper());
    stopButton.addEventListener('click', async () => stopScraper());
});
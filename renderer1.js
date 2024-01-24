document.addEventListener('DOMContentLoaded', () => {
    const keywords = ['outcall', 'incall'];
    const flagged_keywords = ['outcall']
    const search_mode = false
    const search_text = ''
    const inclusive_search = false
    const path = 'C:\\Users\\kskos\\PycharmProjects\\hsi_backend_test\\result'
    const cityYesBackpage = 'florida';
    const cityMegapersonals = 'daytona';
    const cityEscortalligator = 'daytona';
    const citySkipthegames = 'bonita springs'
    const cityEros = 'miami'

    // Find the button elements by their IDs
    const yesbackpageButton = document.getElementById('yesbackpage');
    const megapersonalsButton = document.getElementById('megapersonals');
    const escortalligatorButton = document.getElementById('escortalligator');
    const skipthegamesButton = document.getElementById('skipthegames');
    const erosButton = document.getElementById('eros');
    const stopButton =document.getElementById("stopbutton");

    // Reusable function to handle button click event
    const handleButtonClick = async (city, scraperEndpoint) => {
        try {
            // Make a request to your Flask API
            const url = `http://localhost:3000/start_scraper?city=${encodeURIComponent(city)}
                                                                        &keywords=${encodeURIComponent(keywords.join(','))}
                                                                        &flagged_keywords=${encodeURIComponent(flagged_keywords.join(','))}
                                                                        &search_mode=${encodeURIComponent(search_mode)}
                                                                        &search_text=${encodeURIComponent(search_text)}
                                                                        &inclusive_search=${encodeURIComponent(inclusive_search)}
                                                                        &path=${encodeURIComponent(path)}`;
            const response = await fetch(url);

            // Check if the response is OK
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            // Parse the response as JSON
            const data = await response.json();

            // Check if the response contains an error key
            if (data.error) {
                throw new Error(`Server error: ${data.error}`);
            }

            // Display the data in your Electron app (you can use DOM manipulation here)
            console.log(`Response: ${JSON.stringify(data)}`);
        } catch (error) {
            console.error('Error:', error.message);
        }
    };

    const stopScraper = async() => {
        try {
            // Make a request to your Flask API
            const url = `http://localhost:3000/stop_scraper`;
            const response = await fetch(url);

            // Check if the response is OK
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            // Parse the response as JSON
            const data = await response.json();

            // Check if the response contains an error key
            if (data.error) {
                throw new Error(`Server error: ${data.error}`);
            }

            // Display the data in your Electron app (you can use DOM manipulation here)
            console.log(`Response: ${JSON.stringify(data)}`);
        } catch (error) {
            console.error('Error:', error.message);
        }
    };


    // Add click event listeners to the buttons
    yesbackpageButton.addEventListener('click', async () => handleButtonClick(cityYesBackpage, 'yesbackpage_scraper'));
    megapersonalsButton.addEventListener('click', async () => handleButtonClick(cityMegapersonals, 'megapersonals_scraper'));
    escortalligatorButton.addEventListener('click', async () => handleButtonClick(cityEscortalligator, 'escortalligator_scraper'));
    skipthegamesButton.addEventListener('click', async () => handleButtonClick(citySkipthegames, 'skipthegames_scraper'));
    erosButton.addEventListener('click', async () => handleButtonClick(cityEros, 'eros_scraper'));
    stopButton.addEventListener('click', async () => stopScraper())
});
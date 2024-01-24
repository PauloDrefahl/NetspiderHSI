document.addEventListener('DOMContentLoaded', () => {
    // Find the button element by its ID
    const yesbackpageButton = document.getElementById('yesbackpage');
    const megapersonalsButton = document.getElementById('megapersonals')

    // Add a click event listener to the button
    yesbackpageButton.addEventListener('click', async () => {
        try {
            // Make a request to your Flask API
            const keywords = ['outcall','incall']
            const city = 'florida'
            const url = `http://localhost:5000/yesbackpage_scraper?city=${encodeURIComponent(city)}&keywords=${encodeURIComponent(keywords.join(','))}`;


            const response = await fetch(url)
            // Check if the response is OK
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            // Access the response data
            const data = await response.json();

            // Display the data in your Electron app (you can use DOM manipulation here)
            console.log(`Number of Posts: ${data.numPosts}`);

        } catch (error) {
            console.error('Error:', error);
        }
    });

    megapersonalsButton.addEventListener('click', async () =>{

    });
});
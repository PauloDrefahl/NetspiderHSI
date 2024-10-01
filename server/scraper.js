document.addEventListener("DOMContentLoaded", function () {

    // ---- data extraction ----    
        // start and stop button
        start_button = document.getElementById("startButton");
        stop_button = document.getElementById("stopButton");
    
        // selection of Website to scrape
        // website will be argument for the route with start webscraping
        var escort_alligator = document.getElementById("website1");
        var mega_personals = document.getElementById("website2");
        var skip_the_games = document.getElementById("website3");
        var yes_back_page = document.getElementById("website4");
        var eros = document.getElementById("website5");
    

        // file / keyword data
        var keyword_file = document.getElementById("file1");
        var keyset_file = document.getElementById("file2");
        var result_directory = document.getElementById("file3");
    
    
        // location data
    
    
    
        // option data
    
    
    // EOF data declare / extraction
    
    // ---- event listeners for buttons -------
    
    // Think about what interactions the user has to make that involve functions and information from our python program
    
        // --- START BUTTON IMPLEMENTATION ---

        // Function to determine which website is selected
    function getSelectedWebsite() {
        if (escort_alligator.checked) return 'esal';
        if (mega_personals.checked) return 'mepe';
        if (skip_the_games.checked) return 'skga';
        if (yes_back_page.checked) return 'yepa';
        if (eros.checked) return 'eros';
        return null; // or some default value
    }

    // Event listener for the start button
    start_button.addEventListener("click", function () {
        var selectedWebsite = getSelectedWebsite();
        if (!selectedWebsite) {
            console.error('No website selected');
            return; // Stop the function if no website is selected
        }

        var requestInfo = {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({/**scraper options */})
        }

        // request to run scraper
        fetch(`http://localhost:5000/api/${selectedWebsite}`, requestInfo)
        .then(response => response.json()) 
        .then(data => {/** handling the response of python program about the scraper */})
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // --- STOP BUTTON IMPLEMENTATION --- 

    // Event listener for the stop button
    stop_button.addEventListener("click", function () {
        // similar fetch request as in the start button
        // depending on how your API handles stopping the scraper
        var requestInfo = {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({/** */})
        }

        // request to run scraper
        fetch('http://localhost:5000/api/stop_scraper', requestInfo)
        //handle response from scraper  
        .then(response => response.json()) 
        .then(data => {/**handling the response of python program about the scraper's termination */})
        .catch(error => {
            // Handle any errors
            console.error('Error:', error);
        });
    });

    
    /*
        // website event listener to return location lists
        escort_alligator.addEventListener("click", function () {
            
            var requestInfo = {
                method: "POST",
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({/** *//*})/*
            }
    
            // request to run scraper
            fetch('http://localhost:5000/api/esal', requestInfo)
            //handle response from scraper  
            .then(response => response.json()) 
            .then(data => {/** *//*})/*
            .catch(error => {
                // Handle any errors
                console.error('Error:', error);
            });
        })
    
        mega_personals.addEventListener("click", function () {
            
            var requestInfo = {
                method: "POST",
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({/** *//*})/*
            }
    
            // request to run scraper
            fetch('http://localhost:5000/api/mepe', requestInfo)
            //handle response from scraper  
            .then(response => response.json()) 
            .then(data => {/** *//*})
            .catch(error => {
                // Handle any errors
                console.error('Error:', error);
            });
        })
    
        skip_the_games.addEventListener("click", function () {
            
            var requestInfo = {
                method: "POST",
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({/** *//*})
            }
    
            // request to run scraper
            fetch('http://localhost:5000/api/skga', requestInfo)
            //handle response from scraper  
            .then(response => response.json()) 
            .then(data => {/** *//*})
            .catch(error => {
                // Handle any errors
                console.error('Error:', error);
            });
        })
    
        yes_back_page.addEventListener("click", function () {
            
            var requestInfo = {
                method: "POST",
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({/** *//*})
            }
    
            // request to run scraper
            fetch('http://localhost:5000/api/yepa', requestInfo)
            //handle response from scraper  
            .then(response => response.json()) 
            .then(data => {/** *//*})
            .catch(error => {
                // Handle any errors
                console.error('Error:', error);
            });
        })
    
        eros.addEventListener("click", function () {
            
            var requestInfo = {
                method: "POST",
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({/** *//*})
            }
    
            // request to run scraper
            fetch('http://localhost:5000/api/eros', requestInfo)
            //handle response from scraper  
            .then(response => response.json()) 
            .then(data => {/** *//*})
            .catch(error => {
                // Handle any errors
                console.error('Error:', error);
            });
        })
    
        // buttons to start or stop scraper
    
        start_button.addEventListener("click", function () {
            
            var requestInfo = {
                method: "POST",
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({/** *//*})
            }
    
            // request to run scraper
            fetch('http://localhost:5000/get_text', requestInfo)
            //handle response from scraper  
            .then(response => response.json()) 
            .then(data => {/** *//*})
            .catch(error => {
                // Handle any errors
                console.error('Error:', error);
            });

            */
    });
    
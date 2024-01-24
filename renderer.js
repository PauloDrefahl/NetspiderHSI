// renderer.js
document.getElementById('loadButton').addEventListener('click', () => { // event listener on load button
    fetch('http://localhost:5000/Kevin') // uses the route flask is using for the get_text
        .then(response => response.text()) // gets the text from flask in form of response
        .then(text => {
            document.getElementById('displayText').innerText = text;  // puts the text into displayText variable in index.html
        })
        .catch(err => console.error('Error fetching text:', err));  // error handling
});
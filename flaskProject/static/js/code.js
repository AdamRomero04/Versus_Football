const searchInput = document.querySelectorAll('.searchInput');
const searchButton = document.getElementById('searchButton');
const searchTerms = []

searchButton.addEventListener('click', function() {
    let leftName = document.getElementById("searchInputLeft").value;
    let rightName = document.getElementById("searchInputRight").value;
    const searchTerms = [leftName, rightName]
    
    const data = {
        searchTerms: searchTerms
    };

    const request = new XMLHttpRequest();
    request.open('POST', '/search');
    request.setRequestHeader('Content-Type', 'application/json');
    request.send(JSON.stringify(data));
    
    const messageContainer = document.getElementById('messageContainer');
    messageContainer.textContent = "Data sent!";
    console.log("js ran")
});




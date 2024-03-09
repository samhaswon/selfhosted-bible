// Minify using: https://www.digitalocean.com/community/tools/minify
/* Get references to the search box, result list, and class selection dropdown */
const searchBox = document.getElementById('search-box');
const searchResults = document.getElementById('search-results');
const versionSelection = document.getElementById('version-selection');

/* Function to fetch search results from the server */
async function fetchSearchResults(query, version) {
    return await fetch(`/search_endpoint/?query=${query}&version=${version}`)
    .then((raw_response) => {
        return raw_response.json()
    }).catch(
        error => {console.log(error);
    });
}

/* Function to update the search results */
function updateResults(results) {
    /* Clear previous results */
    searchResults.innerHTML = '';

    for (let i = 0; i < results.length; i++) {
        const book = results[i][0].substring(0, results[i][0].indexOf(" "));
        const chapter = results[i][0].substring(results[i][0].indexOf(" ") + 1, results[i][0].indexOf(":"));

        const ref = `/goto/?version=${versionSelection.value}&book=${book}&chapter=${chapter}`;
        const ref_child = document.createElement('a');
        ref_child.href = ref;
        ref_child.textContent = results[i][0];

        const li = document.createElement('li');
        li.appendChild(ref_child);
        li.appendChild(document.createTextNode(` ${results[i][1]}`));
        li.appendChild(document.createElement('br'));
        li.appendChild(document.createElement('br'));
        searchResults.appendChild(li);
    }
}

/* Event listeners for input event on the search box */
searchBox.addEventListener('input', (event) => {
    const query = searchBox.value;
    const version = versionSelection.value;
    const searchResults = fetchSearchResults(query, version)
    .then((results) => {
        updateResults(results.results);
    }).catch(
        error => {console.log(error);
    });
});
versionSelection.addEventListener('change', (event) => {
    const query = searchBox.value;
    const version = versionSelection.value;
    const searchResults = fetchSearchResults(query, version)
    .then((results) => {
        updateResults(results.results);
    }).catch((error) => {
        console.log(error);
    });
});

// Add event listener to the list
searchResults.addEventListener('click', function(event) {
    // Check if the clicked element is a list item
    if (event.target.tagName === 'LI') {
        // Get the text content of the clicked list item
        const reference = event.target.textContent.trim();

        // Set the Flask cookie with the reference
        document.cookie = `reference=${reference}; path=/`; // Adjust the path as needed
    }
});
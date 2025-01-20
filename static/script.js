document.getElementById('search-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const query = document.getElementById('search-query').value;

    const response = await fetch(`/search?query=${query}`);
    const data = await response.json();

    const searchResultsDiv = document.getElementById('search-results');
    searchResultsDiv.innerHTML = '';
    if (data.length > 0) {
        data.forEach(result => {
            const resultElement = document.createElement('div');
            resultElement.innerHTML = `<a href="${result.url}" target="_blank">${result.title}</a>`;
            searchResultsDiv.appendChild(resultElement);
        });
    } else {
        searchResultsDiv.textContent = 'לא נמצאו תוצאות חיפוש.';
    }
});

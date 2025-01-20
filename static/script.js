document.getElementById('search-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const query = document.getElementById('search-query').value;

    // שליחת בקשה ל-API
    const response = await fetch(`/search?query=${query}`);
    const data = await response.json();

    // הצגת תוצאות חיפוש
    const searchResultsDiv = document.getElementById('search-results');
    searchResultsDiv.innerHTML = '';
    if (data.length > 0) {
        data.forEach(result => {
            const resultElement = document.createElement('div');
            resultElement.innerHTML = `
                <p>
                    <strong><a href="${result.url}" target="_blank">${result.title}</a></strong><br>
                    מילים מובילות: ${result.top_words}
                </p>
            `;
            searchResultsDiv.appendChild(resultElement);
        });
    } else {
        searchResultsDiv.textContent = 'לא נמצאו תוצאות חיפוש.';
    }
});

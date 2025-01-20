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
            resultElement.innerHTML = `
                <p>
                    <strong><a href="${result.url}" target="_blank">${result.url}</a></strong><br>
                    TF-IDF Score: ${result.tf_idf_score.toFixed(4)}<br>
                    PageRank: ${result.page_rank.toFixed(4)}<br>
                    מילים: ${Object.entries(result.words).map(([word, score]) => `${word} (${score})`).join(', ')}
                </p>
            `;
            searchResultsDiv.appendChild(resultElement);
        });
    } else {
        searchResultsDiv.textContent = 'לא נמצאו תוצאות חיפוש.';
    }
});

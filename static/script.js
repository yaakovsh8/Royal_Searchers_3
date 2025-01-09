document.getElementById('search-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const query = document.getElementById('search-query').value;

    const response = await fetch(`/search?query=${query}`);
    const results = await response.json();

    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    if (results.error) {
        resultsDiv.textContent = results.error;
        return;
    }

    results.forEach(page => {
        const pageElement = document.createElement('div');
        pageElement.innerHTML = `<h3><a href="${page.url}" target="_blank">${page.url}</a></h3><p>${JSON.stringify(page.results)}</p>`;
        resultsDiv.appendChild(pageElement);
    });
});

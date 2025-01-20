const data = [
    { question: "שאלה 1: הרחבות שאילתא ואחזור ממוין", answer: "תוצאה לשאלה 1 חלק 1" },
    { question: "שאלה 2: Link Analysis", answer: "תוצאה לסעיף ב בשאלה 2" },
    { question: "שאלה 3: קדם פרויקט – בדיקת הזחלן", answer: "תוצאה לסעיף א בשאלה 3" },
    // הוסף כאן את שאר השאלות והתשובות
];

document.getElementById("search-button").addEventListener("click", () => {
    const query = document.getElementById("search-input").value.toLowerCase();
    const results = data.filter(item => item.question.toLowerCase().includes(query) || item.answer.toLowerCase().includes(query));
    displayResults(results);
});

function displayResults(results) {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = results.length
        ? results.map(item => `<div class="result"><h3>${item.question}</h3><p>${item.answer}</p></div>`).join("")
        : "<p>לא נמצאו תוצאות</p>";
}

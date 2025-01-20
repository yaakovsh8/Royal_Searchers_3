from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# כל השאלות והתשובות
data = [
    {"question": "שאלה 1: הרחבות שאילתא ואחזור ממוין", "answer": "תוצאה לשאלה 1 חלק 1"},
    {"question": "שאלה 1: הרחבות שאילתא ואחזור ממוין", "answer": "תוצאה לשאלה 1 חלק 2"},
    {"question": "שאלה 1: הרחבות שאילתא ואחזור ממוין", "answer": "תוצאה לשאלה 1 חלק 3"},
    {"question": "שאלה 2: Link Analysis - סעיף א", "answer": "תוצאה לסעיף א בשאלה 2"},
    {"question": "שאלה 2: Link Analysis - סעיף ב", "answer": "תוצאה לסעיף ב בשאלה 2"},
    {"question": "שאלה 3: קדם פרויקט – בדיקת הזחלן - סעיף א", "answer": "תוצאה לסעיף א בשאלה 3"},
    {"question": "שאלה 3: קדם פרויקט – בדיקת הזחלן - סעיף ב", "answer": "תוצאה לסעיף ב בשאלה 3"},
    {"question": "שאלה 3: קדם פרויקט – בדיקת הזחלן - סעיף ג", "answer": "תוצאה לסעיף ג בשאלה 3"},
    {"question": "שאלה 3: קדם פרויקט – בדיקת הזחלן - סעיף ד", "answer": "תוצאה לסעיף ד בשאלה 3"},
    {"question": "שאלה 3: קדם פרויקט – בדיקת הזחלן - סעיף ה", "answer": "תוצאה לסעיף ה בשאלה 3"},
    {"question": "שאלה 4", "answer": "תוצאה לשאלה 4"},
    {"question": "שאלה 5", "answer": "תוצאה לשאלה 5"},
    {"question": "שאלה 6: הצגת התוצרים - סעיף א", "answer": "תוצאה לסעיף א בשאלה 6"},
    {"question": "שאלה 6: הצגת התוצרים - סעיף ב", "answer": "תוצאה לסעיף ב בשאלה 6"},
    {"question": "שאלה 6: הצגת התוצרים - סעיף ג", "answer": "תוצאה לסעיף ג בשאלה 6"},
    {"question": "שאלה 6: הצגת התוצרים - סעיף ד", "answer": "תוצאה לסעיף ד בשאלה 6"},
    {"question": "שאלה 6: הצגת התוצרים - סעיף ה", "answer": "תוצאה לסעיף ה בשאלה 6"}
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    query = request.json.get("query", "").lower()
    results = [item for item in data if query in item["question"].lower() or query in item["answer"].lower()]
    return jsonify(results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

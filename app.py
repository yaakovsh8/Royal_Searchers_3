from flask import Flask, render_template, request, jsonify
from crawler import crawl  # מנוע החיפוש שלך

app = Flask(__name__)

# עמוד הבית עם מנוע החיפוש
@app.route('/')
def index():
    return render_template('index.html')

# עמוד שאלות ותשובות
@app.route('/questions')
def questions():
    return render_template('questions.html')

# API לחיפוש
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    start_url = "https://www.myprotein.co.il/"
    results = crawl(query, start_url, max_page=5)
    return jsonify(results)  # החזרת תוצאות JSON

if __name__ == '__main__':
    app.run(debug=True)

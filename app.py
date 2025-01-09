from flask import Flask, render_template, request, jsonify
from crawler import crawl

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    start_url = "https://www.myprotein.co.il/"
    results = crawl(query, start_url, max_page=5)  # קריאה לקוד שלך
    return jsonify(results)  # החזרת התוצאות ל-JavaScript

if __name__ == '__main__':
    app.run(debug=True)



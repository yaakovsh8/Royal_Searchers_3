from flask import Flask, render_template, request, jsonify
from hw_3 import crawl_all, compute_tf_idf, calculate_page_rank

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/questions')
def questions():
    return render_template('questions.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # זחילה וחישוב TF-IDF
    results = crawl_all()
    tf_idf_scores = compute_tf_idf(query, results)

    # דירוג PageRank
    links_structure = {
        url: [] for url in results.keys()  # יצירת מבנה קישורים
    }
    page_rank = calculate_page_rank(links_structure)

    # עיבוד התוצאות
    ranked_results = sorted(tf_idf_scores.items(), key=lambda x: sum(x[1].values()), reverse=True)
    formatted_results = [
        {
            "url": url,
            "tf_idf_score": sum(scores.values()),
            "page_rank": page_rank.get(url, 0),
            "words": {word: f"{score:.4f}" for word, score in scores.items()}
        }
        for url, scores in ranked_results
    ]

    return jsonify(formatted_results)

if __name__ == '__main__':
    app.run(debug=True)

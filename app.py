from flask import Flask, render_template, request, jsonify
from hw_3 import crawl_all, compute_tf_idf

app = Flask(__name__)

# דף הבית עם מנוע החיפוש
@app.route('/')
def index():
    return render_template('index.html')

# דף שאלות ותשובות
@app.route('/questions')
def questions():
    return render_template('questions.html')

# API לחיפוש
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # זחילה וחישוב TF-IDF
    results = crawl_all()
    tf_idf_scores = compute_tf_idf(query, results)

    # דירוג תוצאות
    ranked_results = sorted(tf_idf_scores.items(), key=lambda x: sum(x[1].values()), reverse=True)

    # פורמט JSON מעודכן
    formatted_results = [
        {
            "url": url,
            "title": f"Total TF-IDF: {sum(scores.values()):.4f}",
            "top_words": ", ".join([f"{word} ({scores[word]:.4f})" for word in scores])
        }
        for url, scores in ranked_results
    ]

    return jsonify(formatted_results)


if __name__ == '__main__':
    app.run(debug=True)

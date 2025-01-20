import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import defaultdict, Counter
from nltk.stem import PorterStemmer
import math
import numpy as np


# פונקציות עיבוד טקסט
def index_words(soup):
    index = {}
    words = re.findall(r'\b\w+(?:-\w+)*\b', soup.get_text())
    for word in words:
        word = word.lower()
        index[word] = index.get(word, 0) + 1
    return index


def apply_stemming(index):
    stemmer = PorterStemmer()
    stemmed_index = {}
    for word, count in index.items():
        stemmed_word = stemmer.stem(word)
        stemmed_index[stemmed_word] = stemmed_index.get(stemmed_word, 0) + count
    return stemmed_index


def remove_stop_words(index):
    stop_words = {
       "a", "about", "above", "after", "again", "all", "am", "an", "and", "any", "are", "as", "at",
       "be", "because", "been", "before", "being", "both", "but", "by", "can", "did", "do", "does",
       "each", "for", "from", "had", "has", "have", "he", "her", "here", "him", "his", "how", "i",
       "if", "in", "is", "it", "its", "me", "more", "most", "my", "no", "not", "of", "on", "or",
       "our", "out", "over", "so", "some", "than", "that", "the", "their", "them", "then", "there",
       "these", "they", "this", "to", "under", "up", "very", "was", "we", "were", "what", "when",
       "where", "which", "who", "why", "will", "with", "you", "your"
    }
    return {word: count for word, count in index.items() if word not in stop_words}


# פונקציית זחילה
def crawl_all():
    specific_urls = [
        "https://www.myprotein.co.il/nutrition/healthy-food-drinks/protein-snacks.list",
        "https://www.myprotein.co.il/clothing/mens/all-tops.list"
    ]
    visited = set()
    results = {}

    for url in specific_urls:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # עיבוד תוכן
            index = index_words(soup)
            index = remove_stop_words(index)
            index = apply_stemming(index)
            results[url] = index
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")

    return results


# חישוב TF-IDF
def compute_tf_idf(query, results):
    query_words = query.lower().split()
    tf_idf_scores = defaultdict(dict)
    num_docs = len(results)

    # ספירת מסמכים לכל מילה בשאילתה
    word_doc_counts = Counter()
    for word in query_words:
        for word_counts in results.values():
            if word in word_counts:
                word_doc_counts[word] += 1

    # חישוב IDF
    idf = {word: math.log(num_docs / (1 + count)) for word, count in word_doc_counts.items()}

    # חישוב TF-IDF לכל מסמך
    for url, word_counts in results.items():
        total_words = sum(word_counts.values())
        for word in query_words:
            if word in word_counts:
                tf = word_counts[word] / total_words
                tf_idf_scores[url][word] = tf * idf[word]

    return tf_idf_scores


# פונקציה לחישוב PageRank
def calculate_page_rank(links_structure, damping_factor=0.85, max_iterations=100, epsilon=1e-6):
    pages = list(links_structure.keys())
    N = len(pages)
    ranks = np.ones(N) / N
    page_index = {page: i for i, page in enumerate(pages)}

    adj_matrix = np.zeros((N, N))
    for page, out_links in links_structure.items():
        if out_links:
            for out_link in out_links:
                if out_link in page_index:
                    adj_matrix[page_index[out_link], page_index[page]] = 1 / len(out_links)

    # טיפול בקודקודים תלויים
    dangling_nodes = np.where(adj_matrix.sum(axis=0) == 0)[0]
    for node in dangling_nodes:
        adj_matrix[:, node] = 1 / N

    # חישוב PageRank
    for iteration in range(max_iterations):
        new_ranks = (1 - damping_factor) / N + damping_factor * adj_matrix @ ranks
        if np.linalg.norm(new_ranks - ranks, 1) < epsilon:
            ranks = new_ranks
            break
        ranks = new_ranks

    return {pages[i]: ranks[i] for i in range(N)}


# פונקציה להצגת נתונים סטטיסטיים
def display_results(query, results, tf_idf_scores):
    print(f"\nתוצאות עבור השאילתה: {query}")
    print("-" * 50)

    for url, word_counts in results.items():
        print(f"כתובת: {url}")
        print("מילים נפוצות:")
        for word, count in Counter(word_counts).most_common(10):
            print(f"  {word}: {count}")
        print()

    print("\nTF-IDF Results:")
    for url, scores in tf_idf_scores.items():
        print(f"כתובת: {url}")
        for word, score in scores.items():
            print(f"  {word}: {score:.4f}")
        print()


# הרצה מקומית
if __name__ == "__main__":
    results = crawl_all()
    search_query = "L T-Shirt"
    tf_idf_scores = compute_tf_idf(search_query, results)
    display_results(search_query, results, tf_idf_scores)

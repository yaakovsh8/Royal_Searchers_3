import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from nltk.stem import PorterStemmer
from collections import defaultdict, Counter
import math

# פונקציות לעיבוד טקסט
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
    start_urls = [
        "https://www.myprotein.co.il/nutrition/healthy-food-drinks/protein-snacks.list",
        "https://www.myprotein.co.il/clothing/mens/all-tops.list"
    ]
    MAX_PAGES = 50  # הגבלת כמות העמודים
    visited = set()
    to_visit = list(start_urls)
    results = {}

    while to_visit and len(visited) < MAX_PAGES:
        url = to_visit.pop(0)
        if url in visited:
            continue

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            index = index_words(soup)
            index = remove_stop_words(index)
            index = apply_stemming(index)
            results[url] = index

            for link in soup.find_all('a', href=True):
                href = link['href']
                if href and not href.startswith('#'):  # דילוג על קישורים ריקים או עוגנים (#)
                    full_url = urljoin(url, href)
                if full_url.startswith("https://www.myprotein.co.il") and full_url not in visited:
                    to_visit.append(full_url)
                    
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")

        visited.add(url)

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

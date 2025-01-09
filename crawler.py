import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from nltk.stem import PorterStemmer
import re

def index_words(soup):
    index = {}
    words = re.findall(r'\w+', soup.get_text())
    for word in words:
        word = word.lower()
        if word in index:
            index[word] += 1
        else:
            index[word] = 1
    return index

def apply_stemming(index):
    stemmer = PorterStemmer()
    stemmed_index = {}
    for word, count in index.items():
        stemmed_word = stemmer.stem(word)
        if stemmed_word in stemmed_index:
            stemmed_index[stemmed_word] += count
        else:
            stemmed_index[stemmed_word] = count
    return stemmed_index


def remove_stop_words(index):
    stop_words = stop_words = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at",
    "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can", "can't", "cannot", "could",
    "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from",
    "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in",
    "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no",
    "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over",
    "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that",
    "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd",
    "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was",
    "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where",
    "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you",
    "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"}

    for stop_word in stop_words:
        if stop_word in index:
            del index[stop_word]
    return index


def search(query, index):

    stemmer = PorterStemmer()
    query_words = re.findall(r'\w+', query.lower())
    print(query)
    results = {}
    for word in query_words:
        word = stemmer.stem(word)
        if word in index:
            results[word] = index[word]
    return results


def search_engine(soup, query):
    index = index_words(soup)
    index = remove_stop_words(index)
    index = apply_stemming(index)
    results = search(query, index)
    return results


def crawl(query, start_url, max_page=20):
    visited = set()
    to_visit = [start_url]
    pages_crawled = 0
    results_list = []  # שמירה של התוצאות

    while to_visit and pages_crawled < max_page:
        url = to_visit.pop(0)
        if url in visited:
            continue

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to fetch {url}: {e}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        if soup is None:
            continue

        results = search_engine(soup, query)
        results_list.append({"url": url, "results": results})

        for link in soup.find_all('a', href=True):
            full_url = urljoin(url, link['href'])
            if full_url not in visited and full_url.startswith("http"):
                to_visit.append(full_url)

        visited.add(url)
        pages_crawled += 1

    return results_list

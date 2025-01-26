from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def crawl_myprotein(query):
    base_url = "https://www.myprotein.co.il"
    search_url = f"{base_url}/search/{query}.list"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    for product in soup.select('.product-list-item'):
        title = product.select_one('.product-title').text.strip() if product.select_one('.product-title') else "No title"
        price = product.select_one('.price').text.strip() if product.select_one('.price') else "No price"
        link = product.select_one('.product-title a')['href'] if product.select_one('.product-title a') else "#"
        results.append({
            "title": title,
            "price": price,
            "link": f"{base_url}{link}"
        })
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return render_template('search.html', error="No query provided", results=None)
    
    # זחילה וחיפוש באתר MyProtein
    results = crawl_myprotein(query)
    if not results:
        return render_template('search.html', error="Failed to retrieve results", results=None)
    
    return render_template('search.html', query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True)

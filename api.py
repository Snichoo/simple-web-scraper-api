from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # Return both the URL and the text content in a dictionary
        return {
            "url": url,
            "content": soup.get_text(separator=' ', strip=True)
        }
    except requests.exceptions.RequestException as e:
        return {
            "url": url,
            "error": f"Error scraping {url}: {str(e)}"
        }

@app.route('/scrape', methods=['POST'])
def scrape():
    if not request.is_json:
        return jsonify({"error": "Invalid input, expecting JSON"}), 400
    
    data = request.get_json()
    urls = data.get('urls', [])
    
    if not isinstance(urls, list):
        return jsonify({"error": "Invalid input, 'urls' should be a list"}), 400
    
    results = {}
    for url in urls:
        results[url] = scrape_content(url)
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

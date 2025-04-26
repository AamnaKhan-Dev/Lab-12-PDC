#app.py
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# ✅ Make sure this matches your actual SolrCloud collection
SOLR_URL = 'http://localhost:8983/solr/books/select'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()

    if not query:
        return jsonify([])

    params = {
        'q': query,  # 🔍 Use a specific field if needed (like 'title:')
        'wt': 'json',
        'df': 'author',
        'rows': 10,
        'shards.tolerant': 'true'
    }

    try:
        solr_response = requests.get(SOLR_URL, params=params)
        solr_response.raise_for_status()
        results = solr_response.json()

        if 'response' in results and 'docs' in results['response']:
            return jsonify(results['response']['docs'])
        else:
            return jsonify([])
    except Exception as e:
        print("[❌] Solr request failed:", e)
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)

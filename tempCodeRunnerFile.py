from flask import Flask, render_template, request, jsonify
from utils import check_ssl, get_dns_info, get_site_title
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    url = data.get('url', '')
    if not url.startswith('http'):
        url = 'http://' + url

    try:
        domain = urlparse(url).netloc
        ssl_result = check_ssl(domain)
        dns_result = get_dns_info(domain)
        title_result = get_site_title(url)

        return jsonify({
            'ssl': ssl_result,
            'dns': dns_result,
            'title': title_result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

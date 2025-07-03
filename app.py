from flask import Flask, render_template, request, jsonify
from utils import check_ssl, get_dns_info, get_site_title
from urllib.parse import urlparse
from datetime import datetime

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

        # Save to logs
        with open("logs.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"[{datetime.now()}] URL: {url}\n")
            log_file.write(f"SSL: {ssl_result}\n")
            log_file.write(f"DNS: {dns_result}\n")
            log_file.write(f"Title: {title_result}\n")
            log_file.write("-" * 40 + "\n")

        return jsonify({
            'ssl': ssl_result,
            'dns': dns_result,
            'title': title_result
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logs')
def show_logs():
    try:
        with open("logs.txt", "r", encoding="utf-8") as log_file:
            content = log_file.read()
        return render_template('logs.html', logs=content)
    except FileNotFoundError:
        return render_template('logs.html', logs="No logs found.")

@app.route('/clear-logs', methods=['POST'])
def clear_logs():
    open("logs.txt", "w", encoding="utf-8").close()
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

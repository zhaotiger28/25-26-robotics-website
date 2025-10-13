"""
u have to run ts for the server
  pip install flask
  py tools/server.py

Open http://127.0.0.1:8000 in your browser.
"""
from flask import Flask, request, send_from_directory, jsonify
from pathlib import Path
from datetime import datetime
import csv

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / 'logs' / 'requests.csv'

app = Flask(__name__, static_folder=str(ROOT), static_url_path='')

@app.route('/api/requests', methods=['POST'])
def add_request():
    data = request.get_json(force=True)
    name = (data.get('name') or '').strip()
    subject = (data.get('subject') or '').strip()
    message = (data.get('message') or '').strip()
    if not name or not subject or not message:
        return jsonify({'success': False, 'error': 'missing_fields'}), 400

    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open('a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.utcnow().isoformat(), name, subject, message])

    return jsonify({'success': True})

# Serve static files
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve(path):
    p = ROOT / path
    if p.exists() and p.is_file():
        return send_from_directory(str(ROOT), path)
    return send_from_directory(str(ROOT), 'index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)

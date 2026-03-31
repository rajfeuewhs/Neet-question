from flask import Flask, render_template, jsonify, request
import requests
import base64
import json
import os

app = Flask(__name__)

# GitHub Details
GITHUB_TOKEN = "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"
REPO_OWNER = "rajfeuewhs"
REPO_NAME = "Neet-question"
GITHUB_BASE = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/data/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/get_config')
def get_config():
    try:
        r = requests.get(f"{GITHUB_BASE}config.json", timeout=10)
        return jsonify(r.json())
    except:
        return jsonify({"error": "Config not found"}), 404

@app.route('/get_test/<path:p>')
def get_test(p):
    try:
        r = requests.get(f"{GITHUB_BASE}{p}.json", timeout=10)
        return jsonify(r.json())
    except:
        return jsonify([])

@app.route('/save_test', methods=['POST'])
def save_test():
    data = request.json
    subject = data['subject']
    chapter = data['chapter'].replace(" ", "_")
    test_name = data['test_name'].replace(" ", "_")
    questions = data['questions']
    
    # Path: data/subject/chapter/test.json
    path = f"data/{subject}/{chapter}/{test_name}.json"
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path}"
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # JSON ko sundar format mein badalna
    content_str = json.dumps(questions, indent=2)
    encoded_content = base64.b64encode(content_str.encode()).decode()

    payload = {
        "message": f"Admin: Added {test_name} to {chapter}",
        "content": encoded_content
    }

    # GitHub par file upload karna
    r = requests.put(url, headers=headers, json=payload)
    
    if r.status_code in [200, 201]:
        return jsonify({"success": True, "message": "Test Live Ho Gaya Hai!"})
    else:
        return jsonify({"success": False, "message": r.json().get('message', 'Upload Failed')})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

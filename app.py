from flask import Flask, render_template, jsonify, request
import requests
import base64
import json
import os

app = Flask(__name__)

# GitHub Config
GITHUB_TOKEN = "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"
REPO_OWNER = "rajfeuewhs"
REPO_NAME = "Neet-question"
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/"
RAW_BASE_URL = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/data/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/get_config')
def get_config():
    r = requests.get(f"{RAW_BASE_URL}config.json")
    return jsonify(r.json()) if r.status_code == 200 else jsonify({})

@app.route('/get_test/<path:p>')
def get_test(p):
    r = requests.get(f"{RAW_BASE_URL}{p}.json")
    return jsonify(r.json()) if r.status_code == 200 else jsonify([])

def github_upload(path, content, message):
    url = GITHUB_API_URL + path
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    r = requests.get(url, headers=headers)
    sha = r.json().get('sha') if r.status_code == 200 else None
    payload = {
        "message": message,
        "content": base64.b64encode(content.encode()).decode(),
        "branch": "main"
    }
    if sha: payload["sha"] = sha
    return requests.put(url, headers=headers, json=payload)

@app.route('/save_test', methods=['POST'])
def save_test():
    data = request.json
    sub = data['subject']
    chap = data['chapter'].strip()
    t_name = data['test_name'].strip()
    questions = data['questions']
    
    file_path = f"data/{sub}/{chap.replace(' ', '_')}/{t_name.replace(' ', '_')}.json"
    github_upload(file_path, json.dumps(questions, indent=2), f"Add test: {t_name}")
    
    config_path = "data/config.json"
    r_config = requests.get(RAW_BASE_URL + "config.json")
    config_data = r_config.json() if r_config.status_code == 200 else {}

    if sub not in config_data: config_data[sub] = {}
    if chap not in config_data[sub]: config_data[sub][chap] = []
    
    exists = any(t['name'] == t_name for t in config_data[sub][chap])
    if not exists:
        config_data[sub][chap].append({
            "name": t_name,
            "file": f"{sub}/{chap.replace(' ', '_')}/{t_name.replace(' ', '_')}"
        })
        github_upload(config_path, json.dumps(config_data, indent=2), f"Update config for {t_name}")

    return jsonify({"success": True, "message": "Test Live!"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

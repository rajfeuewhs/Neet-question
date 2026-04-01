from flask import Flask, render_template, jsonify, request
import requests
import base64
import json
import os
import time

app = Flask(__name__)

# Render Secrets
GITHUB_TOKEN = os.environ.get("MY_GITHUB_TOKEN")
REPO_OWNER = "rajfeuewhs"
REPO_NAME = "Neet-question"
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/"
RAW_BASE_URL = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/data/"

@app.route('/')
def index(): return render_template('index.html')

@app.route('/admin')
def admin(): return render_template('admin.html')

@app.route('/get_config')
def get_config():
    try:
        r = requests.get(f"{RAW_BASE_URL}config.json?t={int(time.time())}")
        return jsonify(r.json()) if r.status_code == 200 else jsonify({})
    except: return jsonify({})

@app.route('/get_test/<path:p>')
def get_test(p):
    try:
        r = requests.get(f"{RAW_BASE_URL}{p}.json?t={int(time.time())}")
        return jsonify(r.json()) if r.status_code == 200 else jsonify([])
    except: return jsonify([])

def github_upload(path, content, message):
    if not GITHUB_TOKEN: return None
    url = GITHUB_API_URL + path
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    r = requests.get(url, headers=headers)
    sha = r.json().get('sha') if r.status_code == 200 else None
    payload = {
        "message": message,
        "content": base64.b64encode(content.encode('utf-8')).decode('utf-8'),
        "branch": "main"
    }
    if sha: payload["sha"] = sha
    return requests.put(url, headers=headers, json=payload)

@app.route('/save_test', methods=['POST'])
def save_test():
    try:
        data = request.json
        sub = data['subject'].lower()
        chap = data['chapter'].strip()
        t_name = data['test_name'].strip()
        questions = data['questions']
        unlock_at = data.get('unlock_at', "") # Naya scheduling field

        safe_chap = chap.replace(' ', '_').replace(':', '').replace('__', '_')
        safe_name = t_name.replace(' ', '_')
        file_path = f"data/{sub}/{safe_chap}/{safe_name}.json"
        
        # 1. Upload Questions
        github_upload(file_path, json.dumps(questions, indent=2), f"Add test: {t_name}")
        
        # 2. Update Config
        r_conf = requests.get(f"{RAW_BASE_URL}config.json?t={int(time.time())}")
        config_data = r_conf.json() if r_conf.status_code == 200 else {}

        if sub not in config_data: config_data[sub] = {}
        if chap not in config_data[sub]: config_data[sub][chap] = []
        
        # Update if exists, else add
        found = False
        for t in config_data[sub][chap]:
            if t['name'] == t_name:
                t['unlock_at'] = unlock_at
                found = True
        
        if not found:
            config_data[sub][chap].append({
                "name": t_name,
                "file": f"{sub}/{safe_chap}/{safe_name}",
                "unlock_at": unlock_at
            })
            
        github_upload("data/config.json", json.dumps(config_data, indent=2), f"Update config for {t_name}")
        return jsonify({"success": True})
    except Exception as e: return jsonify({"success": False, "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

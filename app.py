from flask import Flask, render_template, jsonify, request
import requests
import base64
import json
import os
import time

app = Flask(__name__)

# GitHub Config - Ye Render Environment se uthayega
GITHUB_TOKEN = os.environ.get("MY_GITHUB_TOKEN")
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
    # Cache se bachne ke liye timestamp
    try:
        r = requests.get(f"{RAW_BASE_URL}config.json?t={int(time.time())}")
        return jsonify(r.json()) if r.status_code == 200 else jsonify({})
    except:
        return jsonify({})

@app.route('/get_test/<path:p>')
def get_test(p):
    try:
        r = requests.get(f"{RAW_BASE_URL}{p}.json?t={int(time.time())}")
        return jsonify(r.json()) if r.status_code == 200 else jsonify([])
    except:
        return jsonify([])

def github_upload(path, content, message):
    if not GITHUB_TOKEN:
        return None
    url = GITHUB_API_URL + path
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    
    # SHA lena zaroori hai update ke liye
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
        if not GITHUB_TOKEN:
            return jsonify({"success": False, "message": "Token missing in Render!"})

        data = request.json
        sub = data['subject']
        chap = data['chapter'].strip()
        t_name = data['test_name'].strip()
        questions = data['questions']
        
        # Path cleaning logic taaki website dhoond sake
        safe_chap = chap.replace(':', '').replace(' ', '_').replace('__', '_')
        safe_name = t_name.replace(' ', '_')
        file_path = f"data/{sub}/{safe_chap}/{safe_name}.json"
        
        # 1. DPP File Upload
        res1 = github_upload(file_path, json.dumps(questions, indent=2), f"Add test: {t_name}")
        
        if not res1 or res1.status_code not in [200, 201]:
            return jsonify({"success": False, "message": "GitHub File Upload Failed!"})

        # 2. Config Update Logic (Forceful)
        r_config = requests.get(f"{RAW_BASE_URL}config.json?t={int(time.time())}")
        config_data = r_config.json() if r_config.status_code == 200 else {}

        # Ensure keys exist
        if sub not in config_data: config_data[sub] = {}
        if chap not in config_data[sub]: config_data[sub][chap] = []
        
        # Check if already exists
        exists = any(t['name'] == t_name for t in config_data[sub][chap])
        
        if not exists:
            config_data[sub][chap].append({
                "name": t_name,
                "file": f"{sub}/{safe_chap}/{safe_name}"
            })
            # Push updated config to GitHub
            github_upload("data/config.json", json.dumps(config_data, indent=2), f"Update config for {t_name}")

        return jsonify({"success": True, "message": f"Success! {t_name} is now LIVE."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

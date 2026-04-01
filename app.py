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

@app.route('/delete_item', methods=['POST'])
def delete_item():
    try:
        data = request.json
        sub, chap, t_name, target = data.get('subject'), data.get('chapter'), data.get('test_name'), data.get('target')
        r_conf = requests.get(f"{RAW_BASE_URL}config.json?t={int(time.time())}")
        config_data = r_conf.json() if r_conf.status_code == 200 else {}

        if target == 'test' and sub in config_data and chap in config_data[sub]:
            config_data[sub][chap] = [t for t in config_data[sub][chap] if t['name'] != t_name]
            if not config_data[sub][chap]: del config_data[sub][chap]
        elif target == 'chapter' and sub in config_data:
            if chap in config_data[sub]: del config_data[sub][chap]
        elif target == 'subject':
            if sub in config_data: del config_data[sub]

        github_upload("data/config.json", json.dumps(config_data, indent=2), f"Delete {target}")
        return jsonify({"success": True})
    except Exception as e: return jsonify({"success": False, "message": str(e)})

def github_upload(path, content, message):
    if not GITHUB_TOKEN: return None
    url = GITHUB_API_URL + path
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    r = requests.get(url, headers=headers)
    sha = r.json().get('sha') if r.status_code == 200 else None
    payload = {"message": message, "content": base64.b64encode(content.encode('utf-8')).decode('utf-8'), "branch": "main"}
    if sha: payload["sha"] = sha
    return requests.put(url, headers=headers, json=payload)

# Baaki save_test aur get_test routes bhi add kar dena...
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

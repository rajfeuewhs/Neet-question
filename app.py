from flask import Flask, render_template, jsonify, request
import requests, base64, json, os, time

# Static folder support ke liye update
app = Flask(__name__, static_folder='static')

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
        r = requests.get(f"{RAW_BASE_URL}config.json?v={int(time.time())}")
        return jsonify(r.json()) if r.status_code == 200 else jsonify({})
    except: return jsonify({})

@app.route('/get_test/<path:p>')
def get_test(p):
    try:
        url = f"{RAW_BASE_URL}{p}.json" if not p.endswith('.json') else f"{RAW_BASE_URL}{p}"
        r = requests.get(f"{url}?v={int(time.time())}")
        return jsonify(r.json()) if r.status_code == 200 else jsonify([])
    except: return jsonify([])

def github_upload(path, content, message):
    if not GITHUB_TOKEN: return None
    url = GITHUB_API_URL + path
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    r = requests.get(url, headers=headers)
    sha = r.json().get('sha') if r.status_code == 200 else None
    payload = {"message": message, "content": base64.b64encode(content.encode('utf-8')).decode('utf-8'), "branch": "main"}
    if sha: payload["sha"] = sha
    return requests.put(url, headers=headers, json=payload)

@app.route('/save_test', methods=['POST'])
def save_test():
    try:
        data = request.json
        sub = data['subject'].lower().strip()
        chap = data['chapter'].strip() if data['chapter'] else "Direct_Tests"
        t_name = data['test_name'].strip()
        
        safe_chap = chap.replace(' ', '_').replace(':', '')
        safe_name = t_name.replace(' ', '_')
        file_path = f"data/{sub}/{safe_chap}/{safe_name}.json"
        
        github_upload(file_path, json.dumps(data['questions'], indent=2), f"Add {t_name}")
        
        r_conf = requests.get(f"{RAW_BASE_URL}config.json?v={int(time.time())}")
        config_data = r_conf.json() if r_conf.status_code == 200 else {}

        if sub not in config_data: config_data[sub] = {}
        if chap not in config_data[sub]: config_data[sub][chap] = []
        
        config_data[sub][chap] = [t for t in config_data[sub][chap] if t['name'] != t_name]
        config_data[sub][chap].append({
            "name": t_name,
            "file": f"{sub}/{safe_chap}/{safe_name}",
            "unlock_at": data.get('unlock_at', "")
        })
            
        github_upload("data/config.json", json.dumps(config_data, indent=2), "Update Config")
        return jsonify({"success": True})
    except Exception as e: return jsonify({"success": False, "message": str(e)})

@app.route('/delete_item', methods=['POST'])
def delete_item():
    try:
        data = request.json
        sub, chap, t_name, target = data.get('subject'), data.get('chapter'), data.get('test_name'), data.get('target')
        
        r_conf = requests.get(f"{RAW_BASE_URL}config.json?v={int(time.time())}")
        config_data = r_conf.json() if r_conf.status_code == 200 else {}

        if target == 'test':
            real_chap = chap if chap else "Direct_Tests"
            if sub in config_data and real_chap in config_data[sub]:
                config_data[sub][real_chap] = [t for t in config_data[sub][real_chap] if t['name'] != t_name]
                if not config_data[sub][real_chap]: del config_data[sub][real_chap]
        elif target == 'chapter':
            if sub in config_data and chap in config_data[sub]: del config_data[sub][chap]
        elif target == 'subject':
            if sub in config_data: del config_data[sub]

        github_upload("data/config.json", json.dumps(config_data, indent=2), f"Delete {target}")
        return jsonify({"success": True})
    except Exception as e: return jsonify({"success": False, "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

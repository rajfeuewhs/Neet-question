from flask import Flask, render_template, jsonify, request
import requests, base64, json, os, time

app = Flask(__name__)

# GitHub Settings
GITHUB_TOKEN = os.environ.get("MY_GITHUB_TOKEN")
REPO_OWNER = "rajfeuewhs" 
REPO_NAME = "Neet-question"
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/"
RAW_BASE_URL = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/"

@app.route('/')
def index(): return render_template('index.html')

@app.route('/admin')
def admin(): return render_template('admin.html')

# --- CONFIG FETCH ---
@app.route('/get_config')
def get_config():
    try:
        r = requests.get(f"{RAW_BASE_URL}data/config.json?v={int(time.time())}")
        return jsonify(r.json()) if r.status_code == 200 else jsonify({})
    except: return jsonify({})

# --- SAVE TEST (Uploading System) ---
@app.route('/save_test', methods=['POST'])
def save_test():
    try:
        d = request.json # {subject, chapter, test_name, questions, unlock_at}
        filename = f"{d['subject']}_{d['test_name'].replace(' ','_').lower()}.json"
        
        # 1. Upload Test File
        github_upload(f"tests/{filename}", json.dumps(d['questions'], indent=2), f"Add {d['test_name']}")
        
        # 2. Update config.json
        r_cfg = requests.get(f"{RAW_BASE_URL}data/config.json")
        cfg = r_cfg.json() if r_cfg.status_code == 200 else {}
        
        if d['subject'] not in cfg: cfg[d['subject']] = {}
        ch = d['chapter'] if d['chapter'] else "General"
        if ch not in cfg[d['subject']]: cfg[d['subject']][ch] = []
        
        cfg[d['subject']][ch].append({
            "name": d['test_name'],
            "file": filename,
            "unlock_at": d['unlock_at']
        })
        
        github_upload("data/config.json", json.dumps(cfg, indent=2), "Update Config")
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# --- DELETE SYSTEM ---
@app.route('/delete_item', methods=['POST'])
def delete_item():
    try:
        p = request.json # {subject, chapter, test_name, target}
        r_cfg = requests.get(f"{RAW_BASE_URL}data/config.json")
        cfg = r_cfg.json()
        
        if p['target'] == 'test':
            cfg[p['subject']][p['chapter']] = [t for t in cfg[p['subject']][p['chapter']] if t['name'] != p['test_name']]
        elif p['target'] == 'chapter':
            del cfg[p['subject']][p['chapter']]
        elif p['target'] == 'subject':
            del cfg[p['subject']]
            
        github_upload("data/config.json", json.dumps(cfg, indent=2), "Delete Item")
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

def github_upload(path, content, message):
    url = GITHUB_API_URL + path
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    
    # Check if file exists to get SHA
    r = requests.get(url, headers=headers)
    sha = r.json().get('sha') if r.status_code == 200 else None
    
    payload = {
        "message": message,
        "content": base64.b64encode(content.encode('utf-8')).decode('utf-8'),
        "branch": "main"
    }
    if sha: payload["sha"] = sha
    
    return requests.put(url, headers=headers, json=payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, render_template, jsonify, request
import requests, base64, json, os, time

app = Flask(__name__)

# GitHub Settings (Render Environment Variables se aayenge)
GITHUB_TOKEN = os.environ.get("MY_GITHUB_TOKEN")
REPO_OWNER = "rajfeuewhs" # Apna username check kar lena
REPO_NAME = "Neet-question"
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/"
RAW_BASE_URL = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/"

@app.route('/')
def index(): return render_template('index.html')

@app.route('/admin')
def admin(): return render_template('admin.html')

# --- CONFIG MANAGEMENT ---
@app.route('/get_config')
def get_config():
    try:
        r = requests.get(f"{RAW_BASE_URL}data/config.json?v={int(time.time())}")
        return jsonify(r.json()) if r.status_code == 200 else jsonify({})
    except: return jsonify({})

@app.route('/get_test/<path:filename>')
def get_test(filename):
    try:
        r = requests.get(f"{RAW_BASE_URL}tests/{filename}?v={int(time.time())}")
        return jsonify(r.json()) if r.status_code == 200 else jsonify({"error": "Not Found"})
    except: return jsonify({"error": "Error"})

# --- ADMIN ACTIONS (SAVE & DELETE) ---
@app.route('/save_test', methods=['POST'])
def save_test():
    d = request.json # {subject, chapter, test_name, unlock_at, questions}
    filename = f"{d['subject']}_{d['test_name'].replace(' ','_').lower()}.json"
    
    # 1. Upload Test JSON to 'tests/' folder
    github_upload(f"tests/{filename}", json.dumps(d['questions'], indent=2), f"Add {d['test_name']}")
    
    # 2. Update config.json
    r_cfg = requests.get(f"{RAW_BASE_URL}data/config.json")
    cfg = r_cfg.json() if r_cfg.status_code == 200 else {}
    
    if d['subject'] not in cfg: cfg[d['subject']] = {}
    target_chap = d['chapter'] if d['chapter'] else "Direct_Tests"
    if target_chap not in cfg[d['subject']]: cfg[d['subject']][target_chap] = []
    
    cfg[d['subject']][target_chap].append({
        "name": d['test_name'],
        "file": filename,
        "unlock_at": d['unlock_at']
    })
    
    github_upload("data/config.json", json.dumps(cfg, indent=2), "Update Config")
    return jsonify({"success": True})

@app.route('/delete_item', methods=['POST'])
def delete_item():
    p = request.json # {subject, chapter, test_name, target}
    r_cfg = requests.get(f"{RAW_BASE_URL}data/config.json")
    cfg = r_cfg.json()
    
    if p['target'] == 'test':
        tests = cfg[p['subject']][p['chapter']]
        cfg[p['subject']][p['chapter']] = [t for t in tests if t['name'] != p['test_name']]
    elif p['target'] == 'chapter':
        del cfg[p['subject']][p['chapter']]
    elif p['target'] == 'subject':
        del cfg[p['subject']]
        
    github_upload("data/config.json", json.dumps(cfg, indent=2), "Delete Item")
    return jsonify({"success": True})

def github_upload(path, content, message):
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

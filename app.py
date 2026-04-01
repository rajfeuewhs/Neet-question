from flask import Flask, render_template, jsonify, request
import requests, base64, json, os, time

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
    r = requests.get(f"{RAW_BASE_URL}config.json?v={int(time.time())}")
    return jsonify(r.json()) if r.status_code == 200 else jsonify({})

@app.route('/get_bg_config')
def get_bg():
    r = requests.get(f"{RAW_BASE_URL}bg_config.json?v={int(time.time())}")
    return jsonify(r.json()) if r.status_code == 200 else jsonify({"bg_url":"", "logo_url":""})

@app.route('/save_bg_config', methods=['POST'])
def save_bg():
    github_upload("data/bg_config.json", json.dumps(request.json, indent=2), "Update Branding")
    return jsonify({"success": True})

@app.route('/get_test/<path:p>')
def get_test(p):
    url = f"{RAW_BASE_URL}{p}.json" if not p.endswith('.json') else f"{RAW_BASE_URL}{p}"
    r = requests.get(f"{url}?v={int(time.time())}")
    return jsonify(r.json()) if r.status_code == 200 else jsonify([])

def github_upload(path, content, message):
    if not GITHUB_TOKEN: return None
    url = GITHUB_API_URL + path
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    r = requests.get(url, headers=headers); sha = r.json().get('sha') if r.status_code == 200 else None
    p = {"message": message, "content": base64.b64encode(content.encode('utf-8')).decode('utf-8'), "branch": "main"}
    if sha: p["sha"] = sha
    return requests.put(url, headers=headers, json=p)

@app.route('/save_test', methods=['POST'])
def save_test():
    d = request.json; sub = d['subject'].lower().strip(); chap = d['chapter'].strip() or "Direct_Tests"
    t_name = d['test_name'].strip(); sc, sn = chap.replace(' ','_'), t_name.replace(' ','_')
    github_upload(f"data/{sub}/{sc}/{sn}.json", json.dumps(d['questions'], indent=2), f"Add {t_name}")
    rc = requests.get(f"{RAW_BASE_URL}config.json?v={int(time.time())}"); conf = rc.json() if rc.status_code == 200 else {}
    if sub not in conf: conf[sub] = {}
    if chap not in conf[sub]: conf[sub][chap] = []
    conf[sub][chap] = [t for t in conf[sub][chap] if t['name'] != t_name]
    conf[sub][chap].append({"name": t_name, "file": f"{sub}/{sc}/{sn}"})
    github_upload("data/config.json", json.dumps(conf, indent=2), "Update Config")
    return jsonify({"success": True})

@app.route('/delete_item', methods=['POST'])
def delete_item():
    d = request.json; sub, chap, t_name, target = d.get('subject'), d.get('chapter'), d.get('test_name'), d.get('target')
    rc = requests.get(f"{RAW_BASE_URL}config.json?v={int(time.time())}"); conf = rc.json() if rc.status_code == 200 else {}
    if target == 'test':
        c = chap or "Direct_Tests"
        if sub in conf and c in conf[sub]: conf[sub][c] = [t for t in conf[sub][c] if t['name']!=t_name]
    elif target == 'chapter': del conf[sub][chap]
    elif target == 'subject': del conf[sub]
    github_upload("data/config.json", json.dumps(conf, indent=2), f"Del {target}")
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

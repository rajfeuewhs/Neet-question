from flask import Flask, render_template, jsonify, request
import requests, base64, json, os, time

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

# Leaderboard fetch karne ka route
@app.route('/get_leaderboard')
def get_lb():
    try:
        r = requests.get(f"{RAW_BASE_URL}leaderboard.json?v={int(time.time())}")
        return jsonify(r.json()) if r.status_code == 200 else jsonify([])
    except: return jsonify([])

# Apple aur Score update karne ka route
@app.route('/submit_result', methods=['POST'])
def submit_res():
    d = request.json # {username, score, apples}
    try:
        r_lb = requests.get(f"{RAW_BASE_URL}leaderboard.json")
        lb = r_lb.json() if r_lb.status_code == 200 else []
        
        # User update ya add logic
        user = next((item for item in lb if item["username"] == d["username"]), None)
        if user:
            user["apples"] += d["apples"]
            user["score"] += d["score"]
        else:
            lb.append({"username": d["username"], "score": d["score"], "apples": d["apples"]})
        
        # Ranking based on Apples
        lb = sorted(lb, key=lambda x: x['apples'], reverse=True)
        github_upload("data/leaderboard.json", json.dumps(lb, indent=2), "Update Rank")
        return jsonify({"success": True})
    except: return jsonify({"success": False})

def github_upload(path, content, message):
    if not GITHUB_TOKEN: return None
    url = GITHUB_API_URL + path
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    r = requests.get(url, headers=headers); sha = r.json().get('sha') if r.status_code == 200 else None
    p = {"message": message, "content": base64.b64encode(content.encode('utf-8')).decode('utf-8'), "branch": "main"}
    if sha: p["sha"] = sha
    return requests.put(url, headers=headers, json=p)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

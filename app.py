from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)
# Raw GitHub URL (Slash aakhri mein zaroori hai)
GITHUB_BASE = "https://raw.githubusercontent.com/rajfeuewhs/Neet-question/main/data/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_config')
def get_config():
    # Dashboard list yahan se aati hai
    r = requests.get(f"{GITHUB_BASE}config.json")
    return jsonify(r.json())

@app.route('/get_test/<path:p>')
def get_test(p):
    # p = "botany/cell_unit/botany"
    # Result = .../botany/cell_unit/botany.json
    r = requests.get(f"{GITHUB_BASE}{p}.json")
    if r.status_code == 200:
        return jsonify(r.json())
    return jsonify([]), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

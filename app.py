from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)
# GitHub ka sahi Raw URL - aakhri mein slash (/) zaroori hai
GITHUB_BASE = "https://raw.githubusercontent.com/rajfeuewhs/Neet-question/main/data/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_config')
def get_config():
    try:
        r = requests.get(f"{GITHUB_BASE}config.json")
        return jsonify(r.json())
    except:
        return jsonify({"error": "Config not found"}), 404

@app.route('/get_test/<path:p>')
def get_test(p):
    try:
        # P = "botany/cell_unit/botany" tab URL banega: .../botany/cell_unit/botany.json
        url = f"{GITHUB_BASE}{p}.json"
        r = requests.get(url)
        if r.status_code == 200:
            return jsonify(r.json())
        return jsonify([]), 404
    except:
        return jsonify([]), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

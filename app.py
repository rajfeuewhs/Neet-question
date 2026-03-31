from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)

# Raw GitHub URL - Aakhri mein slash (/) zaroori hai
GITHUB_BASE = "https://raw.githubusercontent.com/rajfeuewhs/Neet-question/main/data/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_config')
def get_config():
    try:
        r = requests.get(f"{GITHUB_BASE}config.json", timeout=10)
        if r.status_code == 200:
            return jsonify(r.json())
        return jsonify({"error": "Config file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_test/<path:p>')
def get_test(p):
    try:
        # Path format: botany/cell_unit/dpp1 -> botany/cell_unit/dpp1.json
        url = f"{GITHUB_BASE}{p}.json"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return jsonify(r.json())
        return jsonify({"error": "Test file not found"}), 404
    except Exception as e:
        return jsonify([]), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

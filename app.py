from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)
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
        return jsonify({"error": "Config missing"}), 404

@app.route('/get_test/<path:p>')
def get_test(p):
    try:
        r = requests.get(f"{GITHUB_BASE}{p}.json")
        return jsonify(r.json())
    except:
        return jsonify([]), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

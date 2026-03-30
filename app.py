from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)

# Aapka GitHub Base URL
GITHUB_BASE = "https://raw.githubusercontent.com/rajfeuewhs/Neet-question/main/data/"

@app.route('/')
def index():
    return render_template('index.html')

# Config file fetch karne ke liye
@app.route('/get_config')
def get_config():
    try:
        response = requests.get(f"{GITHUB_BASE}config.json")
        return jsonify(response.json())
    except:
        return jsonify({"error": "Config not found"}), 404

# Specific test fetch karne ke liye
@app.route('/get_test/<path:test_path>')
def get_test(test_path):
    try:
        response = requests.get(f"{GITHUB_BASE}{test_path}.json")
        return jsonify(response.json())
    except:
        return jsonify([]), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

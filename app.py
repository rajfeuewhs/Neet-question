from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)

# Aapka sahi GitHub Base URL
GITHUB_BASE = "https://raw.githubusercontent.com/rajfeuewhs/Neet-question/main/data/"

@app.route('/')
def index():
    return render_template('index.html')

# Naya Route jo Subject, Chapter aur Test Number handle karega
@app.route('/get_test/<subject>/<chapter>/<test_name>')
def get_test(subject, chapter, test_name):
    try:
        path = f"{subject}/{chapter}/{test_name}.json"
        response = requests.get(f"{GITHUB_BASE}{path}")
        if response.status_code == 200:
            return jsonify(response.json())
        return jsonify({"error": "Test not found"}), 404
    except:
        return jsonify([]), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

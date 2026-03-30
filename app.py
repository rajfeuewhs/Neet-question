from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)

# GitHub Repository ka base URL (Jahan aapki JSON files hain)
GITHUB_BASE_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/data/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_test/<category>')
def get_test(category):
    # Category can be: physics, chemistry, botany, zoology, test_180, test_720
    try:
        response = requests.get(f"{GITHUB_BASE_URL}{category}.json")
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True)

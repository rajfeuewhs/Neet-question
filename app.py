from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)

# GitHub ka base URL jahan aapki JSON files hongi
# Badlein: YOUR_USERNAME aur YOUR_REPO ko apne hisaab se
GITHUB_BASE = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/data/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_test/<category>')
def get_test(category):
    try:
        # Subject wise JSON fetch karega (physics.json, botany.json etc.)
        response = requests.get(f"{GITHUB_BASE}{category}.json")
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": "Data load nahi ho paya"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))

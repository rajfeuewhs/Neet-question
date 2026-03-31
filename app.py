from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)

# Raw GitHub URL - Slash zaroori hai
GITHUB_BASE = "https://raw.githubusercontent.com/rajfeuewhs/Neet-question/main/data/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_config')
def get_config():
    try:
        # 5 second ka timeout rakha hai taaki server na fase
        r = requests.get(f"{GITHUB_BASE}config.json", timeout=5)
        if r.status_code == 200:
            return jsonify(r.json())
        return jsonify({"error": "Config file not found on GitHub"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_test/<path:p>')
def get_test(p):
    try:
        # p = "botany/cell_unit/botany" -> botany/cell_unit/botany.json
        url = f"{GITHUB_BASE}{p}.json"
        r = requests.get(url, timeout=5)
        
        if r.status_code == 200:
            return jsonify(r.json())
        
        # Agar file nahi mili toh empty array [] bhejte hain
        return jsonify([]), 404
    except Exception as e:
        return jsonify([]), 500

if __name__ == '__main__':
    # Render ya local host dono ke liye sahi port
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

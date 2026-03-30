from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)

# Aapki repository ka sahi URL
GITHUB_BASE = "https://raw.githubusercontent.com/rajfeuewhs/Neet-question/main/data/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_test/<category>')
def get_test(category):
    try:
        # Subject wise JSON fetch karega
        response = requests.get(f"{GITHUB_BASE}{category}.json")
        
        if response.status_code == 200:
            content = response.text.strip()
            # Agar file khali hai toh khali array bhejho
            if not content or content == "":
                return jsonify([])
            
            # JSON load karke bhejo
            return jsonify(response.json())
        else:
            return jsonify({"error": f"File '{category}.json' nahi mili"}), 404
            
    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify([]) # Error par app na ruke isliye [] bhej rahe hain

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

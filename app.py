from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)

# GITHUB_BASE ko maine yahan sahi kar diya hai
GITHUB_BASE = "https://raw.githubusercontent.com/rajfeuewhs/Neet-question/main/data/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_test/<category>')
def get_test(category):
    try:
        # Subject wise JSON fetch karega (physics.json, botany.json etc.)
        response = requests.get(f"{GITHUB_BASE}{category}.json")
        
        # Check karein ki GitHub ne file sahi se di hai ya nahi
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"File '{category}.json' nahi mili"}), 404
            
    except Exception as e:
        return jsonify({"error": "Data load karne mein server error"}), 500

if __name__ == '__main__':
    # Render aur Local dono ke liye compatible port logic
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

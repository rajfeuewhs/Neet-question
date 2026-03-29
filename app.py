from flask import Flask, render_template, request, jsonify
import pdfplumber
import re
import os

app = Flask(__name__)

# PDF se questions nikalne ka logic
def extract_neet_questions(pdf_path):
    questions = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        
        # Regex: Yeh Q1. ya 1. jaise questions ko dhoondta hai
        # Options A) B) C) D) ko bhi extract karta hai
        blocks = re.split(r'\n(?=\d+[\.\)])', text) 
        
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 2:
                q_text = lines[0]
                opts = [l.strip() for l in lines if re.match(r'^[A-D][\)\.]', l.strip())]
                
                if len(opts) >= 4:
                    questions.append({
                        "q": q_text,
                        "options": opts[:4],
                        "ans": 0 # Default (Isse baad mein verify kar sakte hain)
                    })
    except Exception as e:
        print(f"Error: {e}")
    return questions

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    
    file = request.files['file']
    path = "temp_test.pdf"
    file.save(path)
    
    data = extract_neet_questions(path)
    os.remove(path) # Process ke baad delete kar do
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
import pdfplumber
import re

app = Flask(__name__)

def extract_questions(pdf_path):
    questions = []
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"

    # Basic Regex: Yeh Q1, Q2 ya 1. 2. jaise patterns dhoondta hai
    # Note: PDF ka format alag hone par regex badalna pad sakta hai
    q_blocks = re.split(r'\n(?=\d+\.|\dQ\d+|Question \d+)', full_text)

    for block in q_blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 2:
            question_text = lines[0]
            options = [l for l in lines if re.match(r'^[A-D]\)|^\([a-d]\)', l.strip())]
            if len(options) >= 4:
                questions.append({
                    "q": question_text,
                    "options": options[:4],
                    "ans": 0 # Default answer (A), isse baad mein manually update kar sakte hain
                })
    return questions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file", 400
    file = request.files['file']
    file.save("temp.pdf")
    data = extract_questions("temp.pdf")
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

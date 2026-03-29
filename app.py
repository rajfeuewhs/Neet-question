import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
import pdfplumber
import os
import json

app = Flask(__name__)

# Render ke environment variable se key uthayega
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_questions_from_ai(raw_text):
    prompt = f"""
    Analyze this raw text from a NEET DPP PDF. 
    Extract all questions and their options. 
    Format the output as a STRICT JSON array of objects.
    
    Rules:
    1. Each object: {{"id": int, "q": "text", "options": ["A", "B", "C", "D"], "correct_ans": int}}
    2. 'correct_ans' is index (A=0, B=1, C=2, D=3).
    3. Find the 'Answer Key' at the end of text to fill 'correct_ans'.
    4. If options are jumbled (like A, C, B, D), sort them as A, B, C, D.
    5. Keep LaTeX math formulas as they are.

    TEXT:
    {raw_text}
    """
    
    response = model.generate_content(prompt)
    # JSON clean karne ke liye logic
    text_res = response.text.strip()
    if "```json" in text_res:
        text_res = text_res.split("```json")[1].split("```")[0]
    
    return json.loads(text_res)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    
    file = request.files['file']
    full_text = ""
    
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                full_text += (page.extract_text() or "") + "\n"
        
        # AI Processing
        questions_data = get_questions_from_ai(full_text)
        return jsonify(questions_data)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "AI could not process this PDF"}), 500

if __name__ == '__main__':
    # Local testing ke liye port 5000, Render auto-handle karega
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

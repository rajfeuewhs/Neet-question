from flask import Flask, render_template, request, jsonify
import pdfplumber
import re
import os

app = Flask(__name__)

def clean_text(text):
    # Faltu spaces aur junk characters hatane ke liye
    return re.sub(r'\s+', ' ', text).strip()

def extract_advanced(pdf_path):
    questions = []
    full_text = ""
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"

        # 1. Sabse pehle poore text ko clean karo
        if not full_text.strip():
            return {"error": "PDF is empty or Image-based (Scanned)"}

        # 2. Split Logic: Ye 1., Q1., Question 1:, [1] sabko handle karega
        # Pattern: Naya sawal wahan shuru hota hai jahan Number ke baad . ya ) ho
        q_pattern = r'\n(?=\d+[\.\)\s\-]|Q(?:uestion)?\s*\d+[\.\)\s\-])'
        blocks = re.split(q_pattern, full_text)

        for block in blocks:
            if len(block.strip()) < 10: continue
            
            # Options nikalne ka logic (A/B/C/D ya 1/2/3/4 in brackets/dots)
            # Pattern: (A) ya A. ya A) 
            opt_pattern = r'[\(\[]?[A-D1-4][\)\.\s\]]\s*|[A-D]\s+[\u2022\-\>]'
            
            # Question text wo hai jo pehle option se pehle aata hai
            parts = re.split(opt_pattern, block)
            
            if len(parts) > 1:
                question_body = clean_text(parts[0])
                # Baki bache hue parts options hain
                options_found = [clean_text(p) for p in parts[1:] if p.strip()]
                
                if len(options_found) >= 2:
                    questions.append({
                        "q": question_body,
                        "options": options_found[:4], # Sirf pehle 4 options lo
                        "ans": 0 # Default Index
                    })

        print(f"--- Perfect Checker Log ---")
        print(f"Blocks detected: {len(blocks)}")
        print(f"Final Questions: {len(questions)}")
        
        return questions

    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def handle_upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    
    file = request.files['file']
    temp_name = "test_upload.pdf"
    file.save(temp_name)
    
    result = extract_advanced(temp_name)
    
    if os.path.exists(temp_name):
        os.remove(temp_name)
        
    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 422
        
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

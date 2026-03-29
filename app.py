from flask import Flask, render_template, request, jsonify
import pdfplumber
import re
import os

app = Flask(__name__)

# Ye function PDF se questions nikalne ki koshish karta hai
def extract_neet_questions(pdf_path):
    questions = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        # Debugging: Terminal mein dikhayega kitna text mila
        print(f"--- Extraction Started ---")
        print(f"Total characters found in PDF: {len(text)}")

        if len(text) < 50:
            print("Error: PDF mein text nahi mila (Shayad ye scanned image PDF hai)")
            return []

        # Regex Update: Ye 1. 2. ya Q1. Q2. dono ko pakdega
        # Hum text ko split kar rahe hain jahan bhi naya question number shuru ho raha hai
        blocks = re.split(r'\n(?=\d+[\.\)\s])', text) 
        print(f"Total potential question blocks: {len(blocks)}")

        for block in blocks:
            lines = [l.strip() for l in block.strip().split('\n') if l.strip()]
            if len(lines) >= 2:
                q_text = lines[0]
                # A) B) C) D) ya (A) (B) (C) (D) patterns dhoondna
                opts = [l for l in lines if re.match(r'^[\(\[]?[A-D][\)\.\s\]]', l)]
                
                if len(opts) >= 2: # Kam se kam 2 options milne par add karein
                    questions.append({
                        "q": q_text,
                        "options": opts[:4],
                        "ans": 0 # Default (Manually verify karna hoga baad mein)
                    })
        
        print(f"Successfully extracted {len(questions)} questions.")
        print(f"--- Extraction Finished ---")

    except Exception as e:
        print(f"System Error: {str(e)}")
    
    return questions

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Temporary save karein process karne ke liye
    temp_path = "temp_test.pdf"
    file.save(temp_path)
    
    data = extract_neet_questions(temp_path)
    
    # File delete karein taaki memory bhar na jaye
    if os.path.exists(temp_path):
        os.remove(temp_path)
    
    if not data:
        return jsonify({"error": "PDF se questions nahi nikal paye. Format check karein."}), 422

    return jsonify(data)

if __name__ == '__main__':
    # Threaded=True se performance behtar hoti hai
    app.run(debug=True, port=5000)

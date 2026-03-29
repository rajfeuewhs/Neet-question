from flask import Flask, render_template, request, jsonify
import pdfplumber
import re
import os

app = Flask(__name__)

def clean_txt(t):
    return re.sub(r'\s+', ' ', t).strip()

def extract_advanced_dpp(pdf_path):
    questions = []
    ans_map = {}
    full_text = ""
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                full_text += (page.extract_text() or "") + "\n"

        # 1. Answer Key Pehle nikaalo (Page 2 se)
        if "Answer Key" in full_text:
            key_part = full_text.split("Answer Key")[-1]
            # Pattern: Q1 (C) ya Q1 (B)
            key_matches = re.findall(r'Q(\d+)\s*[\(\[]?([A-D])[\)\]]?', key_part)
            for q_num, char in key_matches:
                ans_map[int(q_num)] = ord(char.upper()) - ord('A')

        # 2. Questions Split karo (Sirf Answer Key se pehle wala part)
        content_for_qs = full_text.split("Answer Key")[0]
        # Pattern: Jo "Q" aur "Number" se shuru ho
        q_blocks = re.split(r'\n(?=Q\d+)', content_for_qs)

        q_id = 1
        for block in q_blocks:
            if not block.strip() or len(block) < 10: continue

            # --- SMART OPTION EXTRACTION ---
            # Hum block ko split karenge jahan bhi (A), (B), (C), (D) mile
            parts = re.split(r'\(([A-D])\)', block)
            
            # parts[0] hamesha question text hoga
            q_text = clean_txt(parts[0])
            # Q1, Q2 jaisa prefix hatao text se
            q_text = re.sub(r'^Q\d+\s*', '', q_text)

            options_list = []
            # parts mein pattern aisa hota hai: [text, 'A', opt_val, 'B', opt_val...]
            for i in range(2, len(parts), 2):
                options_list.append(clean_txt(parts[i]))

            if len(options_list) >= 2:
                questions.append({
                    "id": q_id,
                    "q": q_text,
                    "options": options_list[:4],
                    "correct_ans": ans_map.get(q_id, 0)
                })
                q_id += 1

        return questions
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def index(): return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    temp = "dpp_temp.pdf"
    file.save(temp)
    data = extract_advanced_dpp(temp)
    os.remove(temp)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

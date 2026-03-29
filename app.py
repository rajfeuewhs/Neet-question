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

        # 1. Answer Key Extraction [cite: 64]
        # Page 2 par "Answer Key" ke niche se answers uthana [cite: 54-74]
        key_part = full_text.split("Answer Key")[-1]
        key_matches = re.findall(r'Q(\d+)\s*\n?\s*[\(\[]?([A-D])[\)\]]?', key_part)
        for q_num, char in key_matches:
            ans_map[int(q_num)] = ord(char.upper()) - ord('A')

        # 2. Question Blocks (Q1 to Q10) [cite: 4, 10, 16, 21, 26, 30, 31, 38, 39, 45]
        content_for_qs = full_text.split("Answer Key")[0]
        q_blocks = re.split(r'\n(?=Q\d+)', content_for_qs)

        q_id = 1
        for block in q_blocks:
            if not block.strip() or len(block) < 10: continue

            # Question text nikalna (Pehle option se pehle wala part)
            # Pattern: (A) ya (B) ya (C) ya (D) [cite: 6, 12, 17, 23, 27]
            split_at_opt = re.split(r'\(([A-D])\)', block)
            
            # parts[0] is the question text
            q_text = clean_txt(split_at_opt[0])
            q_text = re.sub(r'^Q\d+\s*', '', q_text) # Q1, Q2 hatana [cite: 4, 10]

            # Options ko dictionary mein daalna taaki order sahi ho sake
            # Example: Q2 mein C pehle hai B baad mein [cite: 13, 14]
            temp_options = {}
            for i in range(1, len(split_at_opt), 2):
                label = split_at_opt[i] # A, B, C, or D
                val = clean_txt(split_at_opt[i+1])
                temp_options[label] = val

            # Hamesha A, B, C, D ke order mein hi list banegi
            final_options = []
            for label in ['A', 'B', 'C', 'D']:
                if label in temp_options:
                    final_options.append(temp_options[label])

            if len(final_options) >= 2:
                questions.append({
                    "id": q_id,
                    "q": q_text,
                    "options": final_options,
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
    temp = "dpp_final.pdf"
    file.save(temp)
    data = extract_advanced_dpp(temp)
    if os.path.exists(temp): os.remove(temp)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

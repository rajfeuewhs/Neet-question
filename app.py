import fitz  # PyMuPDF
import re
import json

# -------------------------------
# STEP 1: Extract text properly
# -------------------------------
def extract_text_blocks(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""

    for page in doc:
        blocks = page.get_text("blocks")
        
        # Sort blocks left to right, top to bottom
        blocks.sort(key=lambda b: (b[1], b[0]))
        
        for b in blocks:
            full_text += b[4] + "\n"

    return full_text


# -------------------------------
# STEP 2: Extract Questions
# -------------------------------
def extract_questions(text):
    pattern = r'(Q\d+.*?)(?=Q\d+|Answer Key|$)'
    matches = re.findall(pattern, text, re.DOTALL)

    questions = []

    for m in matches:
        questions.append(m.strip())

    return questions


# -------------------------------
# STEP 3: Extract Options
# -------------------------------
def extract_options(q_text):
    options = re.findall(r'\([A-D]\)\s*.*?(?=\([A-D]\)|$)', q_text, re.DOTALL)
    return [opt.strip() for opt in options]


# -------------------------------
# STEP 4: Extract Answer Key
# -------------------------------
def extract_answers(text):
    answers = {}

    match = re.search(r'Answer Key(.*)', text, re.DOTALL | re.IGNORECASE)
    if not match:
        return answers

    key_text = match.group(1)

    pairs = re.findall(r'Q(\d+)\s*\(?([A-D0-9]+)\)?', key_text)

    for q, ans in pairs:
        answers[int(q)] = ans

    return answers


# -------------------------------
# STEP 5: Build Final Data
# -------------------------------
def build_data(pdf_path):
    text = extract_text_blocks(pdf_path)

    questions = extract_questions(text)
    answers = extract_answers(text)

    final_data = []

    for q in questions:
        q_no_match = re.search(r'Q(\d+)', q)
        if not q_no_match:
            continue

        q_no = int(q_no_match.group(1))
        options = extract_options(q)

        # Remove options from question text
        clean_question = re.split(r'\([A-D]\)', q)[0].strip()

        final_data.append({
            "question_no": q_no,
            "question": clean_question,
            "options": options,
            "answer": answers.get(q_no, "N/A")
        })

    return final_data


# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    pdf_path = "your_file.pdf"  # <-- yaha apna PDF name daal

    data = build_data(pdf_path)

    # Save JSON
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("✅ Done! Output saved in output.json")

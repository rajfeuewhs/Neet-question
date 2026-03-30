import re
import pdfplumber

def extract_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            t = page.extract_text(x_tolerance=2, y_tolerance=2)
            if t:
                text += t + "\n"
    return text


def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'(Q\d+)', r'\n\1', text)
    text = re.sub(r'\((A|B|C|D)\)', r'\n(\1)', text)
    return text


def extract_questions(text):
    pattern = r'(Q\d+.*?)(?=Q\d+|Answer Key|$)'
    matches = re.findall(pattern, text, re.DOTALL)

    questions = []

    for q in matches:
        q_no = re.search(r'Q\d+', q).group()
        options = re.findall(r'\([A-D]\).*?(?=\([A-D]\)|$)', q)
        q_text = re.sub(r'\([A-D]\).*', '', q).strip()

        questions.append({
            "question_no": q_no,
            "question": q_text,
            "options": options
        })

    return questions


def extract_answers(text):
    answers = {}
    matches = re.findall(r'(Q\d+)\s*\(?([A-D])\)?', text)

    for q, ans in matches:
        answers[q] = ans

    return answers


def merge_qna(questions, answers):
    for q in questions:
        q_no = q["question_no"]
        q["answer"] = answers.get(q_no, "N/A")
    return questions

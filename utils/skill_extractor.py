import re


SKILL_PATTERNS = {
    "Python": [r"\bpython\b"],
    "C": [r"\bc\b"],
    "C++": [r"\bc\+\+\b"],
    "Java": [r"\bjava\b"],
    "HTML": [r"\bhtml\b"],
    "CSS": [r"\bcss\b"],
    "JavaScript": [r"\bjavascript\b"],
    "SQL": [r"\bsql\b"],

    "Machine Learning": [
        r"\bmachine learning\b",
        r"\bml\b"
    ],

    "Artificial Intelligence": [
        r"\bartificial intelligence\b",
        r"\bai\b"
    ],

    "Natural Language Processing": [
        r"\bnatural language processing\b",
        r"\bnlp\b"
    ],

    "Streamlit": [r"\bstreamlit\b"],

    "Git": [r"\bgit\b"],

    "GitHub": [
        r"\bgithub\b",
        r"\bgit hub\b"
    ],

    "Data Structures": [
        r"\bdata structures\b"
    ],

    "Pandas": [r"\bpandas\b"],
    "NumPy": [r"\bnumpy\b"],
    "Scikit-learn": [
        r"\bscikit[- ]learn\b"
    ]
}


def extract_skills(text):
    text = text.lower()

    found_skills = []

    for skill, patterns in SKILL_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text):
                found_skills.append(skill)
                break

    return found_skills
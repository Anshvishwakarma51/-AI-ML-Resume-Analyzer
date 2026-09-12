import re


SKILLS = [
    "python",
    "c",
    "c++",
    "java",
    "html",
    "css",
    "javascript",
    "sql",
    "machine learning",
    "artificial intelligence",
    "natural language processing",
    "nlp",
    "streamlit",
    "git",
    "github",
    "data structures",
    "pandas",
    "numpy",
    "scikit-learn"
]


def extract_skills(text):
    text = text.lower()

    found_skills = []

    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills
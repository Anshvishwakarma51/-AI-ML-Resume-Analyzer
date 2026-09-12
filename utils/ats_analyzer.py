import re


# Important technical and professional keywords
IMPORTANT_KEYWORDS = [
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
    "data structures",
    "data analysis",
    "streamlit",
    "git",
    "github",
    "pandas",
    "numpy",
    "scikit-learn",
    "problem solving",
    "communication",
    "teamwork",
    "software development",
    "application development",
    "deep learning",
    "tensorflow",
    "pytorch",
    "database",
    "statistics"
]


def extract_keywords(text):
    text = text.lower()

    found_keywords = []

    for keyword in IMPORTANT_KEYWORDS:
        pattern = r"\b" + re.escape(keyword) + r"\b"

        if re.search(pattern, text):
            found_keywords.append(keyword)

    return found_keywords


def compare_keywords(resume_text, job_description):
    resume_keywords = set(extract_keywords(resume_text))
    job_keywords = set(extract_keywords(job_description))

    matched_keywords = resume_keywords.intersection(job_keywords)
    missing_keywords = job_keywords - resume_keywords

    if len(job_keywords) > 0:
        keyword_match_percentage = (
            len(matched_keywords) / len(job_keywords)
        ) * 100
    else:
        keyword_match_percentage = 0

    return (
        matched_keywords,
        missing_keywords,
        round(keyword_match_percentage, 2)
    )
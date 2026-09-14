import re


KEYWORD_ALIASES = {
    "ml": "Machine Learning",
    "ai": "Artificial Intelligence",
    "nlp": "Natural Language Processing",
    "git hub": "GitHub",
    "github": "GitHub",
    "sql": "SQL",
    "python": "Python",
    "communication": "Communication",
    "teamwork": "Teamwork",
    "data structures": "Data Structures",
    "streamlit": "Streamlit"
}


IMPORTANT_KEYWORDS = [
    "Python",
    "C",
    "C++",
    "Java",
    "HTML",
    "CSS",
    "JavaScript",
    "SQL",
    "Machine Learning",
    "Artificial Intelligence",
    "Natural Language Processing",
    "Streamlit",
    "Git",
    "GitHub",
    "Data Structures",
    "Data Analysis",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "Problem Solving",
    "Communication",
    "Teamwork",
    "Software Development",
    "Application Development",
    "Deep Learning",
    "TensorFlow",
    "PyTorch",
    "Database",
    "Statistics"
]


def extract_keywords(text):
    text = text.lower()

    found_keywords = []

    for keyword in IMPORTANT_KEYWORDS:
        keyword_lower = keyword.lower()

        # Check full keyword
        pattern = r"\b" + re.escape(keyword_lower) + r"\b"

        if re.search(pattern, text):
            found_keywords.append(keyword)
            continue

        # Check aliases
        for alias, normalized_keyword in KEYWORD_ALIASES.items():

            if normalized_keyword.lower() == keyword_lower:

                alias_pattern = r"\b" + re.escape(alias) + r"\b"

                if re.search(alias_pattern, text):
                    found_keywords.append(keyword)
                    break

    # Remove duplicates
    return list(dict.fromkeys(found_keywords))


def compare_keywords(resume_text, job_description):

    resume_keywords = set(
        extract_keywords(resume_text)
    )

    job_keywords = set(
        extract_keywords(job_description)
    )

    matched_keywords = (
        resume_keywords.intersection(job_keywords)
    )

    missing_keywords = (
        job_keywords - resume_keywords
    )

    if len(job_keywords) > 0:
        keyword_match_percentage = (
            len(matched_keywords)
            / len(job_keywords)
        ) * 100
    else:
        keyword_match_percentage = 0

    return (
        matched_keywords,
        missing_keywords,
        round(keyword_match_percentage, 2)
    )
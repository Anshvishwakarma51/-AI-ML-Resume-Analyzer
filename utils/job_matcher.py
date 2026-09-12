import re


def extract_job_skills(job_description, skills_list):
    job_description = job_description.lower()

    required_skills = []

    for skill in skills_list:
        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, job_description):
            required_skills.append(skill)

    return required_skills


def calculate_match(resume_skills, job_skills):
    resume_skills = set(resume_skills)
    job_skills = set(job_skills)

    matched_skills = resume_skills.intersection(job_skills)
    missing_skills = job_skills - resume_skills

    if len(job_skills) > 0:
        match_percentage = (len(matched_skills) / len(job_skills)) * 100
    else:
        match_percentage = 0

    return matched_skills, missing_skills, match_percentage
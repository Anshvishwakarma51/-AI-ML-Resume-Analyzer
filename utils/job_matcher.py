import re


SKILL_ALIASES = {
    "ml": "Machine Learning",
    "ai": "Artificial Intelligence",
    "nlp": "Natural Language Processing",
    "git hub": "GitHub"
}


def normalize_skill(skill):
    skill_lower = skill.lower().strip()

    if skill_lower in SKILL_ALIASES:
        return SKILL_ALIASES[skill_lower]

    return skill


def extract_job_skills(job_description, skills_list):
    job_description = job_description.lower()

    required_skills = []

    for skill in skills_list:
        normalized_skill = normalize_skill(skill)
        skill_lower = normalized_skill.lower()

        # Check full skill name
        pattern = r"\b" + re.escape(skill_lower) + r"\b"

        if re.search(pattern, job_description):
            required_skills.append(normalized_skill)
            continue

        # Check common abbreviation
        abbreviation_found = False

        for alias, full_skill in SKILL_ALIASES.items():
            if full_skill.lower() == skill_lower:
                alias_pattern = r"\b" + re.escape(alias) + r"\b"

                if re.search(alias_pattern, job_description):
                    required_skills.append(normalized_skill)
                    abbreviation_found = True
                    break

        if abbreviation_found:
            continue

    # Remove duplicates while preserving order
    return list(dict.fromkeys(required_skills))


def calculate_match(resume_skills, job_skills):
    resume_skills = {
        normalize_skill(skill)
        for skill in resume_skills
    }

    job_skills = {
        normalize_skill(skill)
        for skill in job_skills
    }

    matched_skills = resume_skills.intersection(job_skills)
    missing_skills = job_skills - resume_skills

    if len(job_skills) > 0:
        match_percentage = (
            len(matched_skills) / len(job_skills)
        ) * 100
    else:
        match_percentage = 0

    return matched_skills, missing_skills, match_percentage
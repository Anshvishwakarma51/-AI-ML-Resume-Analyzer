def calculate_resume_score(
    resume_text,
    resume_skills,
    match_percentage
):
    resume_lower = resume_text.lower()

    score = 0

    # ==================================================
    # 1. Resume Content Quality - 15 Marks
    # ==================================================

    text_length = len(resume_text.strip())

    if text_length >= 1500:
        score += 15
    elif text_length >= 1200:
        score += 13
    elif text_length >= 900:
        score += 11
    elif text_length >= 600:
        score += 8
    elif text_length >= 300:
        score += 5
    else:
        score += 2


    # ==================================================
    # 2. Technical Skills - 20 Marks
    # ==================================================

    skill_count = len(resume_skills)

    if skill_count >= 12:
        score += 20
    elif skill_count >= 10:
        score += 18
    elif skill_count >= 8:
        score += 16
    elif skill_count >= 6:
        score += 13
    elif skill_count >= 4:
        score += 10
    elif skill_count >= 2:
        score += 6
    else:
        score += 2


    # ==================================================
    # 3. Resume Sections - 15 Marks
    # ==================================================

    sections = [
        "education",
        "skills",
        "project",
        "certification",
        "summary",
        "experience"
    ]

    found_sections = 0

    for section in sections:
        if section in resume_lower:
            found_sections += 1

    section_score = (
        found_sections / len(sections)
    ) * 15

    score += section_score


    # ==================================================
    # 4. Job Relevance - 25 Marks
    # ==================================================

    # Match percentage contributes a maximum of 25 marks.
    job_relevance_score = match_percentage * 0.25

    score += job_relevance_score


    # ==================================================
    # 5. Projects - 10 Marks
    # ==================================================

    if "project" in resume_lower or "projects" in resume_lower:
        score += 10


    # ==================================================
    # 6. Certifications - 5 Marks
    # ==================================================

    if (
        "certification" in resume_lower
        or "certifications" in resume_lower
        or "certificate" in resume_lower
    ):
        score += 5


    # ==================================================
    # 7. Professional Profile - 10 Marks
    # ==================================================

    professional_score = 0

    # Email
    if "@" in resume_text:
        professional_score += 2

    # LinkedIn
    if "linkedin" in resume_lower:
        professional_score += 2

    # GitHub
    if "github" in resume_lower:
        professional_score += 2

    # Summary / Objective
    if (
        "objective" in resume_lower
        or "summary" in resume_lower
        or "profile" in resume_lower
    ):
        professional_score += 2

    # Communication
    if "communication" in resume_lower:
        professional_score += 1

    # Problem solving
    if (
        "problem solving" in resume_lower
        or "problem-solving" in resume_lower
    ):
        professional_score += 1

    score += professional_score


    # ==================================================
    # 8. Missing Important Sections Penalty
    # ==================================================

    # These penalties prevent the score from becoming
    # unrealistically high.

    if (
        "experience" not in resume_lower
        and "internship" not in resume_lower
    ):
        score -= 5

    if (
        "achievement" not in resume_lower
        and "achievements" not in resume_lower
    ):
        score -= 3


    # ==================================================
    # Final Score
    # ==================================================

    score = max(0, min(score, 100))

    return round(score, 2)
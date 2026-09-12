def calculate_resume_score(
    resume_text,
    resume_skills,
    match_percentage
):
    resume_lower = resume_text.lower()

    # Start with 100 and apply quality-based scoring
    score = 0

    # 1. Resume content quality - 15 marks
    text_length = len(resume_text.strip())

    if text_length >= 1200:
        score += 15
    elif text_length >= 900:
        score += 13
    elif text_length >= 600:
        score += 11
    elif text_length >= 300:
        score += 8
    else:
        score += 4

    # 2. Technical skills - 20 marks
    skill_count = len(resume_skills)

    if skill_count >= 10:
        score += 20
    elif skill_count >= 8:
        score += 17
    elif skill_count >= 6:
        score += 14
    elif skill_count >= 4:
        score += 11
    elif skill_count >= 2:
        score += 7
    else:
        score += 3

    # 3. Resume sections - 15 marks
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

    section_score = (found_sections / len(sections)) * 15
    score += section_score

    # 4. Job relevance - 25 marks
    score += match_percentage * 0.25

    # 5. Projects - 10 marks
    if "project" in resume_lower or "projects" in resume_lower:
        score += 10

    # 6. Certifications - 5 marks
    if "certification" in resume_lower or "certifications" in resume_lower:
        score += 5

    # 7. Resume quality checks - 10 marks

    # Contact information
    contact_score = 0

    if "@" in resume_text:
        contact_score += 2

    if "linkedin" in resume_lower:
        contact_score += 2

    if "github" in resume_lower:
        contact_score += 2

    # Career-related information
    if "objective" in resume_lower or "summary" in resume_lower:
        contact_score += 2

    # Problem-solving / soft skills
    if "problem solving" in resume_lower:
        contact_score += 1

    if "communication" in resume_lower:
        contact_score += 1

    score += contact_score

    # Final score
    score = min(score, 100)

    return round(score, 2)
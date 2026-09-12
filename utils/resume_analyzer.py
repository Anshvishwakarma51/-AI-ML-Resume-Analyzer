def analyze_resume(resume_text, resume_skills, missing_skills):
    resume_lower = resume_text.lower()

    strengths = []
    improvements = []
    suggestions = []

    # Strengths
    if len(resume_text.strip()) >= 500:
        strengths.append("Resume contains sufficient content.")

    if len(resume_skills) >= 5:
        strengths.append("Good number of technical skills detected.")

    if "project" in resume_lower or "projects" in resume_lower:
        strengths.append("Project section is present.")

    if "certification" in resume_lower or "certifications" in resume_lower:
        strengths.append("Certification section is present.")

    if "github" in resume_lower:
        strengths.append("GitHub profile is included.")

    if "linkedin" in resume_lower:
        strengths.append("LinkedIn profile is included.")

    # Improvements
    if missing_skills:
        improvements.append(
            "Some skills required by the job description are missing."
        )

    if "experience" not in resume_lower:
        improvements.append(
            "No experience section detected."
        )

    if "internship" not in resume_lower:
        improvements.append(
            "No internship experience detected."
        )

    if "achievement" not in resume_lower and "achievements" not in resume_lower:
        improvements.append(
            "No achievements section detected."
        )

    # Suggestions
    if missing_skills:
        suggestions.append(
            "Consider learning and adding the missing job-related skills."
        )

    if "experience" not in resume_lower:
        suggestions.append(
            "Add internships, training, or relevant practical experience if available."
        )

    if "achievement" not in resume_lower and "achievements" not in resume_lower:
        suggestions.append(
            "Add measurable achievements from projects, academics, or competitions."
        )

    if "project" in resume_lower or "projects" in resume_lower:
        suggestions.append(
            "Describe project technologies, your contribution, and the result achieved."
        )

    return strengths, improvements, suggestions

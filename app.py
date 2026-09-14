import streamlit as st

from utils.resume_parser import extract_text_from_pdf, extract_text_from_docx
from utils.nlp_processor import clean_text
from utils.skill_extractor import extract_skills
from utils.job_matcher import extract_job_skills, calculate_match
from utils.resume_scorer import calculate_resume_score
from utils.resume_analyzer import analyze_resume
from utils.ats_analyzer import compare_keywords
from utils.similarity_analyzer import calculate_text_similarity
from utils.report_generator import generate_report


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI/ML Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #0e1117;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p {
        color: white;
    }

    /* Main title */
    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        color: #a9b1bd;
        font-size: 17px;
        margin-bottom: 30px;
    }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 14px;
        padding: 18px;
        min-height: 120px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    }

    div[data-testid="metric-container"]:hover {
        border-color: #58a6ff;
        transform: translateY(-2px);
        transition: 0.2s ease;
    }

    /* Section headings */
    h2, h3 {
        color: white;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 12px;
    }

    h3 {
        font-size: 22px;
    }

    /* Upload box */
    section[data-testid="stFileUploaderDropzone"] {
        background-color: #161b22;
        border: 1px dashed #484f58;
        border-radius: 14px;
        padding: 10px;
        transition: 0.2s ease;
    }

    section[data-testid="stFileUploaderDropzone"]:hover {
        border-color: #58a6ff;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown(
        "<h1 style='text-align:center;'>📄</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "## AI/ML Resume Analyzer"
    )

    st.caption(
        "NLP • ATS • Machine Learning"
    )

    st.markdown("---")

    st.markdown("### 🏠 Dashboard")

    st.write("📄 Resume Analysis")
    st.write("🎯 Job Matching")
    st.write("🤖 ATS Analysis")
    st.write("🧠 NLP Similarity")

    st.markdown("---")

    st.markdown("### ⚙️ Analysis Features")

    st.write("✅ Resume Text Extraction")
    st.write("✅ Skill Detection")
    st.write("✅ Keyword Matching")
    st.write("✅ TF-IDF Similarity")
    st.write("✅ Resume Scoring")

    st.markdown("---")

    st.markdown("### 👨‍💻 Developed By")

    st.markdown(
        "**Ansh Vishwakarma**"
    )

    st.caption(
        "B.Tech CSE (AI/ML)"
    )

    github_col, linkedin_col = st.columns(2)

    with github_col:

        st.link_button(
            "💻 GitHub",
            "https://github.com/Anshvishwakarma51",
            use_container_width=True
        )

    with linkedin_col:

        st.link_button(
            "🔗 LinkedIn",
            "https://www.linkedin.com/in/anshvishwakarma51/",
            use_container_width=True
        )

    st.markdown("---")

    st.caption(
        "Mini Project • Version 1.0"
    )


# ==================================================
# MAIN HEADER
# ==================================================

st.markdown(
    '<div class="main-title">📄 AI/ML Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Analyze your resume and compare it with a job description using NLP and machine learning techniques.</div>',
    unsafe_allow_html=True
)


# ==================================================
# INPUT FORM
# ==================================================

with st.form("resume_analysis_form"):

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📄 Upload Resume")

        uploaded_file = st.file_uploader(
            "Upload your PDF or DOCX resume",
            type=["pdf", "docx"]
        )

    with col2:

        st.subheader("💼 Job Description")

        job_description = st.text_area(
            "Paste the job description here",
            height=250,
            placeholder="Example: Python Developer with knowledge of Machine Learning, NLP, SQL, Git and Streamlit..."
        )

    st.markdown("")

    analyze_button = st.form_submit_button(
        "🔍 Analyze Resume",
        use_container_width=True
    )


# ==================================================
# ANALYSIS
# ==================================================

if analyze_button:

    # --------------------------------------------------
    # Validate Resume
    # --------------------------------------------------

    if uploaded_file is None:

        st.warning(
            "⚠️ Please upload a PDF or DOCX resume."
        )

        st.stop()


    # --------------------------------------------------
    # Validate Job Description
    # --------------------------------------------------

    if not job_description.strip():

        st.warning(
            "⚠️ Please enter a job description."
        )

        st.stop()


    # --------------------------------------------------
    # Success Message
    # --------------------------------------------------

    st.success(
        f"Resume uploaded successfully: {uploaded_file.name}"
    )


    # ==================================================
    # RESUME PROCESSING
    # ==================================================

    # --------------------------------------------------
    # Extract Resume Text
    # --------------------------------------------------

    if uploaded_file.name.lower().endswith(".pdf"):

        resume_text = extract_text_from_pdf(
            uploaded_file
        )

    else:

        resume_text = extract_text_from_docx(
            uploaded_file
        )


    # --------------------------------------------------
    # Check Extracted Text
    # --------------------------------------------------

    if not resume_text.strip():

        st.error(
            "❌ Unable to extract text from this resume."
        )

        st.stop()


    # --------------------------------------------------
    # Clean Resume Text
    # --------------------------------------------------

    cleaned_text = clean_text(
        resume_text
    )


    # --------------------------------------------------
    # Extract Skills
    # --------------------------------------------------

    resume_skills = extract_skills(
        cleaned_text
    )


    # ==================================================
    # EXTRACTED RESUME TEXT
    # ==================================================

    st.subheader("📋 Extracted Resume Text")

    with st.expander(
        "View extracted resume content"
    ):

        st.text_area(
            "Resume Content",
            resume_text,
            height=300
        )


    # ==================================================
    # RESUME SKILLS
    # ==================================================

    st.subheader("🧠 Resume Skills")

    if resume_skills:

        skill_columns = st.columns(4)

        for index, skill in enumerate(
            resume_skills
        ):

            with skill_columns[index % 4]:

                st.markdown(
                    f"✅ **{skill}**"
                )

    else:

        st.info(
            "No skills detected."
        )


    # ==================================================
    # JOB DESCRIPTION ANALYSIS
    # ==================================================

    cleaned_job_description = clean_text(
        job_description
    )


    # --------------------------------------------------
    # Skills List
    # --------------------------------------------------

    all_skills = [
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
        "Pandas",
        "NumPy",
        "Scikit-learn"
    ]


    # --------------------------------------------------
    # Job Skill Matching
    # --------------------------------------------------

    job_skills = extract_job_skills(
        cleaned_job_description,
        all_skills
    )

    matched_skills, missing_skills, match_percentage = calculate_match(
        resume_skills,
        job_skills
    )


    # --------------------------------------------------
    # ATS Keyword Analysis
    # --------------------------------------------------

    matched_keywords, missing_keywords, keyword_match_percentage = compare_keywords(
        resume_text,
        job_description
    )


    # --------------------------------------------------
    # TF-IDF + COSINE SIMILARITY
    # --------------------------------------------------

    text_similarity_percentage = calculate_text_similarity(
        resume_text,
        job_description
    )


    # --------------------------------------------------
    # RESUME SCORE
    # --------------------------------------------------

    resume_score = calculate_resume_score(
        resume_text,
        resume_skills,
        match_percentage
    )


    # ==================================================
    # RESUME PERFORMANCE
    # ==================================================

    st.subheader("📊 Resume Performance")

    col1, col2, col3, col4 = st.columns(4)


    # Resume Score
    with col1:

        st.metric(
            "📄 Resume Score",
            f"{resume_score}/100"
        )

        st.progress(
            resume_score / 100
        )


    # Job Match
    with col2:

        st.metric(
            "🎯 Job Match",
            f"{match_percentage:.2f}%"
        )

        st.progress(
            match_percentage / 100
        )


    # ATS Match
    with col3:

        st.metric(
            "🤖 ATS Match",
            f"{keyword_match_percentage:.2f}%"
        )

        st.progress(
            keyword_match_percentage / 100
        )


    # NLP Similarity
    with col4:

        st.metric(
            "🧠 NLP Similarity",
            f"{text_similarity_percentage:.2f}%"
        )

        st.progress(
            text_similarity_percentage / 100
        )


    # ==================================================
    # JOB MATCH RESULT
    # ==================================================

    st.subheader("🎯 Job Match Result")


    # --------------------------------------------------
    # Matched Skills
    # --------------------------------------------------

    st.write("### ✅ Matched Skills")

    if matched_skills:

        for skill in sorted(
            matched_skills
        ):

            st.write(
                f"✅ {skill}"
            )

    else:

        st.write(
            "No matching skills found."
        )


    # --------------------------------------------------
    # Missing Skills
    # --------------------------------------------------

    st.write("### ❌ Missing Skills")

    if missing_skills:

        for skill in sorted(
            missing_skills
        ):

            st.write(
                f"❌ {skill}"
            )

    else:

        st.write(
            "No missing skills!"
        )


    # ==================================================
    # ATS KEYWORD ANALYSIS
    # ==================================================

    st.subheader("🤖 ATS Keyword Analysis")

    st.metric(
        "ATS Keyword Match",
        f"{keyword_match_percentage:.2f}%"
    )


    # --------------------------------------------------
    # Matched Keywords
    # --------------------------------------------------

    st.write("### ✅ Matched Keywords")

    if matched_keywords:

        for keyword in sorted(
            matched_keywords
        ):

            st.write(
                f"✅ {keyword}"
            )

    else:

        st.write(
            "No matched keywords found."
        )


    # --------------------------------------------------
    # Missing Keywords
    # --------------------------------------------------

    st.write("### ❌ Missing Keywords")

    if missing_keywords:

        for keyword in sorted(
            missing_keywords
        ):

            st.write(
                f"❌ {keyword}"
            )

    else:

        st.write(
            "No missing keywords!"
        )


    # ==================================================
    # NLP SIMILARITY ANALYSIS
    # ==================================================

    st.subheader(
        "🧠 NLP Similarity Analysis"
    )

    st.write(
        "TF-IDF and Cosine Similarity compare the textual "
        "similarity between the resume and job description."
    )

    st.metric(
        "Resume–Job Description Similarity",
        f"{text_similarity_percentage:.2f}%"
    )

    st.progress(
        text_similarity_percentage / 100
    )


    # ==================================================
    # RESUME ANALYSIS
    # ==================================================

    strengths, improvements, suggestions = analyze_resume(
        resume_text,
        resume_skills,
        missing_skills
    )


    st.subheader(
        "🔍 Resume Analysis"
    )


    # --------------------------------------------------
    # Strengths
    # --------------------------------------------------

    st.write("### 💪 Strengths")

    if strengths:

        for item in strengths:

            st.write(
                f"✅ {item}"
            )

    else:

        st.write(
            "No major strengths detected."
        )


    # --------------------------------------------------
    # Areas to Improve
    # --------------------------------------------------

    st.write(
        "### ⚠️ Areas to Improve"
    )

    if improvements:

        for item in improvements:

            st.write(
                f"⚠️ {item}"
            )

    else:

        st.write(
            "No major improvement areas detected."
        )


    # --------------------------------------------------
    # Suggestions
    # --------------------------------------------------

    st.write("### 💡 Suggestions")

    if suggestions:

        for item in suggestions:

            st.write(
                f"💡 {item}"
            )

    else:

        st.write(
            "No suggestions at this time."
        )


    # ==================================================
    # DOWNLOAD ANALYSIS REPORT
    # ==================================================

    st.subheader(
        "📥 Download Analysis Report"
    )

    report = generate_report(
        resume_name=uploaded_file.name,
        resume_score=resume_score,
        match_percentage=match_percentage,
        keyword_match_percentage=keyword_match_percentage,
        text_similarity_percentage=text_similarity_percentage,
        resume_skills=resume_skills,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        matched_keywords=matched_keywords,
        missing_keywords=missing_keywords,
        strengths=strengths,
        improvements=improvements,
        suggestions=suggestions
    )


    st.download_button(
    label="📥 Download Report",
    data=report,
    file_name="resume_analysis_report.pdf",
    mime="application/pdf",
    use_container_width=True
)

# ==================================================
# PROFESSIONAL FOOTER
# ==================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align: center;">
        <h3>AI/ML Resume Analyzer</h3>
        <p>Intelligent Resume Screening • NLP • Machine Learning</p>
        <p>Developed by <b>Ansh Vishwakarma</b> • B.Tech CSE (AI/ML)</p>
        <p>© 2026 • AI/ML Resume Analyzer</p>
    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# SOCIAL PROFILE BUTTONS
# ==================================================

st.markdown(
    "<div style='text-align: center;'>",
    unsafe_allow_html=True
)

col1, col2, col3, col4, col5 = st.columns(
    [1, 1, 0.5, 1, 1]
)

with col2:

    st.link_button(
        "💻 GitHub",
        "https://github.com/Anshvishwakarma51",
        use_container_width=True
    )

with col4:

    st.link_button(
        "🔗 LinkedIn",
        "https://www.linkedin.com/in/anshvishwakarma51/",
        use_container_width=True
    )

st.markdown(
    "</div>",
    unsafe_allow_html=True
)
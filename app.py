import streamlit as st

from utils.resume_parser import extract_text_from_pdf, extract_text_from_docx
from utils.nlp_processor import clean_text
from utils.skill_extractor import extract_skills
from utils.job_matcher import extract_job_skills, calculate_match
from utils.resume_scorer import calculate_resume_score
from utils.resume_analyzer import analyze_resume
from utils.ats_analyzer import compare_keywords


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI/ML Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# Custom styling
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    .main {
        padding-top: 1.5rem;
    }

    .hero {
        padding: 1.5rem 1.8rem;
        border-radius: 18px;
        border: 1px solid rgba(128,128,128,0.25);
        background: linear-gradient(
            135deg,
            rgba(49,51,63,0.95),
            rgba(30,32,42,0.95)
        );
        margin-bottom: 1.5rem;
    }

    .hero h1 {
        margin: 0;
        font-size: 2.25rem;
    }

    .hero p {
        margin: 0.45rem 0 0;
        opacity: 0.78;
        font-size: 1rem;
    }

    .section-title {
        font-size: 1.35rem;
        font-weight: 700;
        margin-top: 1.2rem;
        margin-bottom: 0.7rem;
    }

    .score-card {
        border: 1px solid rgba(128,128,128,0.25);
        border-radius: 16px;
        padding: 1rem 1.1rem;
        min-height: 125px;
        background: rgba(128,128,128,0.06);
    }

    .score-label {
        font-size: 0.9rem;
        opacity: 0.75;
        margin-bottom: 0.35rem;
    }

    .score-value {
        font-size: 2rem;
        font-weight: 750;
        line-height: 1.1;
    }

    .skill-box {
        border: 1px solid rgba(128,128,128,0.22);
        border-radius: 12px;
        padding: 0.65rem 0.8rem;
        margin: 0.35rem 0;
        background: rgba(128,128,128,0.045);
    }

    .skill-ok {
        border-left: 4px solid #21c55d;
    }

    .skill-missing {
        border-left: 4px solid #ef4444;
    }

    .analysis-box {
        border: 1px solid rgba(128,128,128,0.22);
        border-radius: 14px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.55rem;
        background: rgba(128,128,128,0.04);
    }

    .small-muted {
        opacity: 0.65;
        font-size: 0.85rem;
    }

    div[data-testid="stMetric"] {
        border: 1px solid rgba(128,128,128,0.22);
        border-radius: 14px;
        padding: 0.7rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("## 📄 Resume Analyzer")
    st.caption("AI/ML • NLP • ATS Analysis")

    st.markdown("---")
    st.markdown("### How it works")
    st.markdown(
        """
        1. Upload a resume
        2. Extract resume text
        3. Detect technical skills
        4. Compare with the job description
        5. Analyze ATS keywords
        6. Generate improvement suggestions
        """
    )

    st.markdown("---")
    st.markdown("### Supported files")
    st.write("📕 PDF")
    st.write("📘 DOCX")

    st.markdown("---")
    st.caption("Mini Project • AI/ML Resume Analyzer")


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>📄 AI/ML Resume Analyzer</h1>
        <p>
            Upload your resume and compare it with a job description
            using NLP-based skill and keyword analysis.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Input section
# ---------------------------------------------------------
st.markdown('<div class="section-title">📥 Upload & Job Description</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    uploaded_file = st.file_uploader(
        "📄 Upload your Resume",
        type=["pdf", "docx"],
        help="Upload a PDF or DOCX resume.",
    )

with col2:
    job_description = st.text_area(
        "💼 Paste Job Description",
        height=210,
        placeholder="Paste the complete job description here...",
        help="The analyzer will compare the resume against this job description.",
    )


# ---------------------------------------------------------
# Main processing
# ---------------------------------------------------------
if uploaded_file is not None:

    st.success(f"Resume uploaded successfully: {uploaded_file.name}")

    # Extract resume text
    try:
        if uploaded_file.name.lower().endswith(".pdf"):
            resume_text = extract_text_from_pdf(uploaded_file)
        else:
            resume_text = extract_text_from_docx(uploaded_file)
    except Exception as exc:
        st.error(f"Could not read the resume: {exc}")
        st.stop()

    if not resume_text or not resume_text.strip():
        st.warning("No readable text was found in this resume.")
        st.stop()

    # Clean resume text
    cleaned_text = clean_text(resume_text)

    # Extract resume skills
    resume_skills = list(dict.fromkeys(extract_skills(cleaned_text)))

    # -----------------------------------------------------
    # Extracted resume text
    # -----------------------------------------------------
    st.markdown('<div class="section-title">📋 Extracted Resume Text</div>', unsafe_allow_html=True)

    with st.expander("View extracted resume content", expanded=False):
        st.text_area(
            "Resume Content",
            resume_text,
            height=300,
            label_visibility="collapsed",
        )

    # -----------------------------------------------------
    # Resume skills
    # -----------------------------------------------------
    st.markdown('<div class="section-title">🧠 Resume Skills</div>', unsafe_allow_html=True)

    if resume_skills:
        skill_columns = st.columns(3)
        for index, skill in enumerate(sorted(resume_skills, key=str.lower)):
            with skill_columns[index % 3]:
                st.markdown(
                    f'<div class="skill-box skill-ok">✅ <b>{skill.title()}</b></div>',
                    unsafe_allow_html=True,
                )
    else:
        st.info("No skills detected.")

    # -----------------------------------------------------
    # Job description analysis
    # -----------------------------------------------------
    if job_description.strip():

        cleaned_job_description = clean_text(job_description)

        # Known skills used by the current analyzer.
        all_skills = list(
            dict.fromkeys(
                resume_skills
                + [
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
                    "scikit-learn",
                ]
            )
        )

        # Extract job skills
        job_skills = extract_job_skills(
            cleaned_job_description,
            all_skills,
        )

        # Calculate job match
        matched_skills, missing_skills, match_percentage = calculate_match(
            resume_skills,
            job_skills,
        )

        # ATS analysis
        (
            matched_keywords,
            missing_keywords,
            keyword_match_percentage,
        ) = compare_keywords(
            resume_text,
            job_description,
        )

        # Resume score
        resume_score = calculate_resume_score(
            resume_text,
            resume_skills,
            match_percentage,
        )

        # -------------------------------------------------
        # Performance cards
        # -------------------------------------------------
        st.markdown(
            '<div class="section-title">📊 Resume Performance</div>',
            unsafe_allow_html=True,
        )

        score_col1, score_col2, score_col3 = st.columns(3, gap="medium")

        with score_col1:
            st.markdown(
                f"""
                <div class="score-card">
                    <div class="score-label">📄 Resume Score</div>
                    <div class="score-value">{resume_score:.1f}<span style="font-size:1rem"> / 100</span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.progress(min(max(float(resume_score) / 100, 0), 1))

        with score_col2:
            st.markdown(
                f"""
                <div class="score-card">
                    <div class="score-label">🎯 Job Match</div>
                    <div class="score-value">{match_percentage:.1f}<span style="font-size:1rem">%</span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.progress(min(max(float(match_percentage) / 100, 0), 1))

        with score_col3:
            st.markdown(
                f"""
                <div class="score-card">
                    <div class="score-label">🤖 ATS Match</div>
                    <div class="score-value">{keyword_match_percentage:.1f}<span style="font-size:1rem">%</span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.progress(min(max(float(keyword_match_percentage) / 100, 0), 1))

        # -------------------------------------------------
        # Job match result
        # -------------------------------------------------
        st.markdown(
            '<div class="section-title">🎯 Job Match Result</div>',
            unsafe_allow_html=True,
        )

        matched_col, missing_col = st.columns(2, gap="large")

        with matched_col:
            st.markdown("### ✅ Matched Skills")

            if matched_skills:
                for skill in sorted(set(matched_skills), key=str.lower):
                    st.markdown(
                        f'<div class="skill-box skill-ok">✅ {skill.title()}</div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.info("No matching skills found.")

        with missing_col:
            st.markdown("### ❌ Missing Skills")

            if missing_skills:
                for skill in sorted(set(missing_skills), key=str.lower):
                    st.markdown(
                        f'<div class="skill-box skill-missing">❌ {skill.title()}</div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.success("No missing skills!")

        # -------------------------------------------------
        # ATS keyword analysis
        # -------------------------------------------------
        st.markdown(
            '<div class="section-title">🤖 ATS Keyword Analysis</div>',
            unsafe_allow_html=True,
        )

        st.metric(
            "ATS Keyword Match",
            f"{keyword_match_percentage:.2f}%",
        )
        st.progress(min(max(float(keyword_match_percentage) / 100, 0), 1))

        ats_col1, ats_col2 = st.columns(2, gap="large")

        with ats_col1:
            st.markdown("### ✅ Matched Keywords")

            if matched_keywords:
                for keyword in sorted(set(matched_keywords), key=str.lower):
                    st.markdown(
                        f'<div class="skill-box skill-ok">✅ {keyword.title()}</div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.info("No matched keywords found.")

        with ats_col2:
            st.markdown("### ❌ Missing Keywords")

            if missing_keywords:
                for keyword in sorted(set(missing_keywords), key=str.lower):
                    st.markdown(
                        f'<div class="skill-box skill-missing">❌ {keyword.title()}</div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.success("No missing keywords!")

        # -------------------------------------------------
        # Resume analysis
        # -------------------------------------------------
        strengths, improvements, suggestions = analyze_resume(
            resume_text,
            resume_skills,
            missing_skills,
        )

        st.markdown(
            '<div class="section-title">🔍 Resume Analysis</div>',
            unsafe_allow_html=True,
        )

        analysis_col1, analysis_col2 = st.columns(2, gap="large")

        with analysis_col1:
            st.markdown("### 💪 Strengths")

            if strengths:
                for item in strengths:
                    st.markdown(
                        f'<div class="analysis-box">✅ {item}</div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.info("No major strengths detected.")

        with analysis_col2:
            st.markdown("### ⚠️ Areas to Improve")

            if improvements:
                for item in improvements:
                    st.markdown(
                        f'<div class="analysis-box">⚠️ {item}</div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.success("No major improvement areas detected.")

        st.markdown("### 💡 Suggestions")

        if suggestions:
            for item in suggestions:
                st.markdown(
                    f'<div class="analysis-box">💡 {item}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.success("No suggestions at this time.")

    else:
        st.info("👆 Upload your resume and paste a job description to start the complete analysis.")

else:
    st.info("👆 Upload a PDF or DOCX resume to begin.")

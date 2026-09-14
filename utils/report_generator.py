from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether
)


def generate_report(
    resume_name,
    resume_score,
    match_percentage,
    keyword_match_percentage,
    text_similarity_percentage,
    resume_skills,
    matched_skills,
    missing_skills,
    matched_keywords,
    missing_keywords,
    strengths,
    improvements,
    suggestions
):

    # --------------------------------------------------
    # Create PDF in memory
    # --------------------------------------------------

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm
    )

    # --------------------------------------------------
    # Styles
    # --------------------------------------------------

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        alignment=TA_CENTER,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        "SubtitleCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.grey,
        spaceAfter=18
    )

    section_style = ParagraphStyle(
        "SectionCustom",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        spaceBefore=14,
        spaceAfter=8
    )

    subsection_style = ParagraphStyle(
        "SubsectionCustom",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        spaceBefore=7,
        spaceAfter=5
    )

    normal_style = ParagraphStyle(
        "NormalCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        spaceAfter=4
    )

    footer_style = ParagraphStyle(
        "FooterCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.grey
    )

    # --------------------------------------------------
    # Story
    # --------------------------------------------------

    story = []

    # --------------------------------------------------
    # Header
    # --------------------------------------------------

    story.append(
        Paragraph(
            "AI/ML RESUME ANALYZER",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Resume Analysis & Job Matching Report",
            subtitle_style
        )
    )

    # --------------------------------------------------
    # Resume Information
    # --------------------------------------------------

    story.append(
        Paragraph(
            "📄 Resume Information",
            section_style
        )
    )

    resume_info = Table(
        [
            ["Resume Name", resume_name],
        ],
        colWidths=[42 * mm, 125 * mm]
    )

    resume_info.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EAF2F8")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9.5),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D0D7DE")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    story.append(resume_info)

    # --------------------------------------------------
    # Performance Summary
    # --------------------------------------------------

    story.append(
        Paragraph(
            "📊 Resume Performance",
            section_style
        )
    )

    performance_data = [
        [
            "📄 Resume Score",
            "🎯 Job Match",
            "🤖 ATS Match",
            "🧠 NLP Similarity"
        ],
        [
            f"{resume_score}/100",
            f"{match_percentage:.2f}%",
            f"{keyword_match_percentage:.2f}%",
            f"{text_similarity_percentage:.2f}%"
        ]
    ]

    performance_table = Table(
        performance_data,
        colWidths=[42 * mm, 42 * mm, 42 * mm, 42 * mm]
    )

    performance_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#161B22")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D0D7DE")),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )

    story.append(performance_table)

    # --------------------------------------------------
    # Helper function for bullet lists
    # --------------------------------------------------

    def add_bullet_section(title, items, bullet="•"):

        story.append(
            Paragraph(
                title,
                subsection_style
            )
        )

        if items:

            for item in sorted(items):

                story.append(
                    Paragraph(
                        f"{bullet} {item}",
                        normal_style
                    )
                )

        else:

            story.append(
                Paragraph(
                    "No items detected.",
                    normal_style
                )
            )

    # --------------------------------------------------
    # Resume Skills
    # --------------------------------------------------

    story.append(
        Paragraph(
            "🧠 Resume Skills",
            section_style
        )
    )

    add_bullet_section(
        "Detected Skills",
        resume_skills,
        "✓"
    )

    # --------------------------------------------------
    # Job Match Analysis
    # --------------------------------------------------

    story.append(
        Paragraph(
            "🎯 Job Match Analysis",
            section_style
        )
    )

    add_bullet_section(
        "✅ Matched Skills",
        matched_skills,
        "✓"
    )

    add_bullet_section(
        "❌ Missing Skills",
        missing_skills,
        "⚠"
    )

    # --------------------------------------------------
    # ATS Analysis
    # --------------------------------------------------

    story.append(
        Paragraph(
            "🤖 ATS Keyword Analysis",
            section_style
        )
    )

    story.append(
        Paragraph(
            f"<b>ATS Keyword Match:</b> "
            f"{keyword_match_percentage:.2f}%",
            normal_style
        )
    )

    add_bullet_section(
        "✅ Matched Keywords",
        matched_keywords,
        "✓"
    )

    add_bullet_section(
        "❌ Missing Keywords",
        missing_keywords,
        "⚠"
    )

    # --------------------------------------------------
    # NLP Similarity
    # --------------------------------------------------

    story.append(
        Paragraph(
            "🧠 NLP Similarity Analysis",
            section_style
        )
    )

    story.append(
        Paragraph(
            "TF-IDF and Cosine Similarity compare the textual "
            "similarity between the resume and job description.",
            normal_style
        )
    )

    story.append(
        Paragraph(
            f"<b>Resume–Job Description Similarity:</b> "
            f"{text_similarity_percentage:.2f}%",
            normal_style
        )
    )

    # --------------------------------------------------
    # Resume Analysis
    # --------------------------------------------------

    story.append(
        Paragraph(
            "🔍 Resume Analysis",
            section_style
        )
    )

    add_bullet_section(
        "💪 Strengths",
        strengths,
        "✓"
    )

    add_bullet_section(
        "⚠️ Areas to Improve",
        improvements,
        "⚠"
    )

    add_bullet_section(
        "💡 Suggestions",
        suggestions,
        "•"
    )

    # --------------------------------------------------
    # Footer
    # --------------------------------------------------

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "AI/ML Resume Analyzer",
            footer_style
        )
    )

    story.append(
        Paragraph(
            "Intelligent Resume Screening • NLP • Machine Learning",
            footer_style
        )
    )

    story.append(
        Paragraph(
            "Developed by Ansh Vishwakarma • B.Tech CSE (AI/ML)",
            footer_style
        )
    )

    story.append(
        Paragraph(
            "© 2026 • AI/ML Resume Analyzer",
            footer_style
        )
    )

    # --------------------------------------------------
    # Build PDF
    # --------------------------------------------------

    doc.build(story)

    buffer.seek(0)

    return buffer.getvalue()
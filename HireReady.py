import google.generativeai as genai
import json
import PyPDF2
import docx
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


# ------------------ Utility Functions ------------------

def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def read_docx(file):
    doc = docx.Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text


def load_resume(uploaded_file):
    if uploaded_file.name.endswith('.pdf'):
        return read_pdf(uploaded_file)
    elif uploaded_file.name.endswith('.docx'):
        return read_docx(uploaded_file)
    else:
        st.error("Unsupported file format")
        return None


# ------------------ PDF Generator ------------------

def generate_updated_resume(resume_text, match_analysis):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=40, leftMargin=40,
                            topMargin=60, bottomMargin=40)
    styles = getSampleStyleSheet()

    header_style = styles['Heading1']
    header_style.fontSize = 16
    header_style.spaceAfter = 18
    header_style.textColor = colors.HexColor('#1a1a1a')

    section_header_style = ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading2'],
        fontSize=13,
        spaceAfter=12,
        textColor=colors.HexColor('#ff6600'),
    )

    bullet_style = ParagraphStyle(
        name='BulletStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        spaceAfter=6,
    )

    recommendation_style = ParagraphStyle(
        name='RecommendationStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#444444'),
        leftIndent=25,
        spaceAfter=4
    )

    content = []
    content.append(Paragraph("Updated Resume", header_style))
    content.append(Spacer(1, 12))

    resume_parts = resume_text.split("\n")
    current_section = ""
    bullets = []

    def flush_bullets():
        for bullet in bullets:
            content.append(Paragraph(f"• {bullet.strip()}", bullet_style))
        bullets.clear()

    common_sections = ['EXPERIENCE', 'EDUCATION', 'SKILLS', 'PROJECTS', 'CERTIFICATIONS', 'SUMMARY', 'OBJECTIVE']

    for line in resume_parts:
        line = line.strip()
        if not line:
            continue

        is_section = line.isupper() or any(section in line.upper() for section in common_sections)

        if is_section:
            flush_bullets()
            current_section = line
            content.append(Spacer(1, 12))
            content.append(Paragraph(current_section, section_header_style))
        else:
            bullets.append(line)

    flush_bullets()

    if match_analysis.get('ats_optimization_suggestions'):
        content.append(Spacer(1, 20))
        content.append(Paragraph("ATS Optimization Recommendations", section_header_style))
        content.append(Spacer(1, 10))
        for suggestion in match_analysis.get('ats_optimization_suggestions', []):
            if isinstance(suggestion, dict):
                section = suggestion.get('section', '')
                suggested = suggestion.get('suggested_change', '')
                keywords = ', '.join(suggestion.get('keywords_to_add', []))
                reason = suggestion.get('reason', '')
            else:
                section = "General"
                suggested = str(suggestion)
                keywords = ''
                reason = ''

            content.append(Paragraph(f"• Section: {section}", recommendation_style))
            content.append(Paragraph(f"  Suggestion: {suggested}", recommendation_style))
            if keywords:
                content.append(Paragraph(f"  Keywords: {keywords}", recommendation_style))
            if reason:
                content.append(Paragraph(f"  Reason: {reason}", recommendation_style))
            content.append(Spacer(1, 6))

    doc.build(content)
    buffer.seek(0)
    return buffer


# ------------------ Gemini API Wrapper ------------------

class GeminiAnalyzer:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("models/gemini-2.5-pro")

    def generate_json(self, prompt: str):
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()

            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].strip()

            return json.loads(text)
        except Exception as e:
            st.error(f"Gemini response parsing error: {e}")
            return {}

    def analyze_job(self, job_description: str):
        prompt = f"""
        Analyze this job description and return a JSON object with:
        {{
          "technical_skills": [],
          "soft_skills": [],
          "years_experience": "",
          "education_requirements": "",
          "key_responsibilities": [],
          "company_culture": "",
          "certifications": [],
          "industry_type": "",
          "job_level": "",
          "technologies": []
        }}
        Job Description:
        {job_description}
        """
        return self.generate_json(prompt)

    def analyze_resume(self, resume_text: str):
        prompt = f"""
        Analyze this resume and return a JSON object with:
        {{
          "technical_skills": [],
          "soft_skills": [],
          "years_experience": "",
          "education": "",
          "achievements": [],
          "competencies": [],
          "industry_experience": "",
          "leadership_experience": "",
          "technologies_used": [],
          "projects": []
        }}
        Resume:
        {resume_text}
        """
        return self.generate_json(prompt)

    def analyze_match(self, job_analysis: dict, resume_analysis: dict):
        prompt = f"""
        Compare this job and resume. Return a JSON object like:
        {{
          "overall_match_percentage": "85%",
          "matching_skills": [],
          "missing_skills": [],
          "skills_gap_analysis": {{"technical_skills": "", "soft_skills": ""}},
          "experience_match_analysis": "",
          "education_match_analysis": "",
          "recommendations_for_improvement": [],
          "ats_optimization_suggestions": [],
          "key_strengths": "",
          "areas_of_improvement": ""
        }}
        Job: {json.dumps(job_analysis, indent=2)}
        Resume: {json.dumps(resume_analysis, indent=2)}
        """
        return self.generate_json(prompt)


class GeminiCoverLetter:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("models/gemini-2.5-pro")

    def generate_cover_letter(self, job_analysis, resume_analysis, match_analysis, tone="professional"):
        prompt = f"""
        Write a {tone} cover letter using:
        Job: {json.dumps(job_analysis, indent=2)}
        Resume: {json.dumps(resume_analysis, indent=2)}
        Match: {json.dumps(match_analysis, indent=2)}
        Requirements:
        - Personalized and concise
        - Highlight strongest matches
        - Address gaps
        - Be ATS-friendly
        - Include a strong call to action
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            st.error(f"Error generating cover letter: {e}")
            return ""


# ------------------ Streamlit UI ------------------

def main():
    st.set_page_config(page_title="HireReady", layout="wide")

    # Custom CSS for dark minimal theme
    st.markdown("""
        <style>
        body { background-color: #0f0f0f; color: #e5e5e5; }
        .stApp { background-color: #121212; }
        h1, h2, h3, h4, h5, h6 { color: #ff6600; }
        .stTextInput, .stTextArea, .stFileUploader, .stButton>button {
            border-radius: 8px;
        }
        .stButton>button {
            background-color: #ff6600;
            color: white;
            border: none;
        }
        .stButton>button:hover {
            background-color: #e55d00;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("HireReady – AI Resume Optimizer")

    st.caption("Refine your resume, match it with job descriptions, and generate professional cover letters powered by **Gemini AI**.")

    api_key = st.sidebar.text_input("Gemini API Key", type="password")
    if not api_key:
        st.warning("Enter your Gemini API key to begin.")
        return

    analyzer = GeminiAnalyzer(api_key)
    cover_letter_gen = GeminiCoverLetter(api_key)

    col1, col2 = st.columns(2)
    with col1:
        job_desc = st.text_area("Job Description", height=300)
    with col2:
        resume_file = st.file_uploader("Upload Resume (.pdf or .docx)", type=["pdf", "docx"])

    if job_desc and resume_file:
        with st.spinner("Analyzing your job and resume..."):
            resume_text = load_resume(resume_file)
            job_analysis = analyzer.analyze_job(job_desc)
            resume_analysis = analyzer.analyze_resume(resume_text)
            match_analysis = analyzer.analyze_match(job_analysis, resume_analysis)

        if not job_analysis or not resume_analysis or not match_analysis:
            st.error("Could not complete analysis. Please verify your API key and input data.")
            return

        st.header("Analysis Overview")

        col1, col2, col3 = st.columns(3)
        col1.metric("Match %", match_analysis.get("overall_match_percentage", "N/A"))
        col2.metric("Matching Skills", len(match_analysis.get("matching_skills", [])))
        col3.metric("Missing Skills", len(match_analysis.get("missing_skills", [])))

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Skills", "Experience & Education", "Recommendations", "Cover Letter", "Updated Resume"
        ])

        with tab1:
            st.subheader("Matching Skills")
            for skill in match_analysis.get("matching_skills", []):
                st.success(skill)

            st.subheader("Missing Skills")
            for skill in match_analysis.get("missing_skills", []):
                st.warning(skill)

            data = pd.DataFrame({
                "Type": ["Matching", "Missing"],
                "Count": [len(match_analysis.get("matching_skills", [])),
                          len(match_analysis.get("missing_skills", []))]
            })
            fig = px.bar(data, x="Type", y="Count", color="Type", title="Skills Overview",
                         color_discrete_sequence=["#ff6600", "#444444"])
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.write("### Experience Match")
            st.write(match_analysis.get("experience_match_analysis", ""))
            st.write("### Education Match")
            st.write(match_analysis.get("education_match_analysis", ""))

        with tab3:
            st.write("### Recommendations")
            for r in match_analysis.get("recommendations_for_improvement", []):
                st.info(str(r))

            st.write("### ATS Optimization Suggestions")
            for r in match_analysis.get("ats_optimization_suggestions", []):
                st.warning(str(r))

        with tab4:
            tone = st.selectbox("Select Tone", ["Professional", "Friendly", "Confident", "Enthusiastic"])
            if st.button("Generate Cover Letter"):
                with st.spinner("Creating cover letter..."):
                    letter = cover_letter_gen.generate_cover_letter(
                        job_analysis, resume_analysis, match_analysis, tone.lower())
                    st.text_area("Generated Cover Letter", letter, height=400)
                    st.download_button("Download Cover Letter", letter, "cover_letter.txt")

        with tab5:
            updated_resume = generate_updated_resume(resume_text, match_analysis)
            st.download_button("Download Updated Resume", updated_resume, "updated_resume.pdf",
                               mime="application/pdf")


if __name__ == "__main__":
    main()

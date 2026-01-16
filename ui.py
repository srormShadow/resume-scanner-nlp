import streamlit as st
import tempfile
import os

from extractor import extract_text, UnsupportedFileFormatError
from preprocess import preprocess_text
from keywords import extract_keywords
from matcher import (
    calculate_match_score,
    calculate_section_based_score,
    compare_keywords,
    missing_keywords_by_section
)

st.set_page_config(page_title="Resume Scanner", layout="centered")

st.title("📄 Resume Scanner (ATS Keyword Matching)")
st.write("Upload your resume and paste a job description to check ATS match score.")

# Inputs
resume_file = st.file_uploader(
    "Upload Resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

jd_text = st.text_area(
    "Paste Job Description",
    height=200
)

# Action
if st.button("Analyze Resume"):

    if not resume_file or not jd_text.strip():
        st.warning("Please upload a resume and paste a job description.")
    else:
        try:
            # ---- Save uploaded file with correct extension
            ext = os.path.splitext(resume_file.name)[1]

            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
                tmp.write(resume_file.read())
                resume_path = tmp.name

            # ---- Extract + preprocess
            resume_text = extract_text(resume_path)
            resume_clean = preprocess_text(resume_text)
            jd_clean = preprocess_text(jd_text)

            # ---- Safety check
            if not resume_clean.strip():
                st.error("⚠️ Resume text could not be processed. The PDF may be image-based.")
                os.remove(resume_path)
                st.stop()

            if not jd_clean.strip():
                st.error("⚠️ Job description text is empty after preprocessing.")
                os.remove(resume_path)
                st.stop()

            # ---- Keyword extraction
            resume_keywords = extract_keywords(resume_clean)
            jd_keywords = extract_keywords(jd_clean)

            # ---- Similarity scores
            overall_score = calculate_match_score(resume_clean, jd_clean)
            section_scores = calculate_section_based_score(resume_clean, jd_clean)

            # ---- Keyword comparison (with skill grouping)
            matched, missing, extra = compare_keywords(
                resume_keywords, jd_keywords
            )

            missing_by_section = missing_keywords_by_section(resume_clean, jd_clean)

            os.remove(resume_path)

            # Output
            st.subheader(f"✅ Overall Match Score: {section_scores['overall']}%")

            st.markdown("### 📊 Section Scores")
            st.write(f"**Skills Match:** {section_scores['skills']}%")
            st.write(f"**Experience Match:** {section_scores['experience']}%")
            st.write(f"**Tools Match:** {section_scores['tools']}%")

            st.markdown("## ❌ Missing Keywords to Better Match the JD")

            st.markdown("### 🧠 Skills")
            st.write(
                missing_by_section["skills"]
                if missing_by_section["skills"]
                else "No major skill gaps found"
            )

            st.markdown("### 🏗️ Experience")
            st.write(
                missing_by_section["experience"]
                if missing_by_section["experience"]
                else "No major experience gaps found"
            )

            st.markdown("### 🧰 Tools & Technologies")
            st.write(
                missing_by_section["tools"]
                if missing_by_section["tools"]
                else "No major tools gaps found"
            )

        except UnsupportedFileFormatError:
            st.error("❌ Unsupported file format. Please upload a valid PDF or DOCX resume.")

        except ValueError as e:
            st.error(f"⚠️ Processing error: {str(e)}")

        except Exception as e:
            st.error("⚠️ An unexpected error occurred while processing the resume.")
            st.exception(e)

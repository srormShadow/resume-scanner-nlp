import streamlit as st
from extractor import extract_text
from preprocess import preprocess_text
from keywords import extract_keywords
from matcher import calculate_match_score, compare_keywords
import tempfile
import os

st.set_page_config(page_title="Resume Scanner", layout="centered")

st.title("📄 Resume Scanner (ATS Keyword Matching)")
st.write("Upload your resume and paste a job description to check ATS match score.")

resume_file = st.file_uploader(
    "Upload Resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

jd_text = st.text_area(
    "Paste Job Description",
    height=200
)

if st.button("Analyze Resume"):
    if not resume_file or not jd_text.strip():
        st.warning("Please upload a resume and paste a job description.")
    else:
        try:
            # Preserve file extension
            file_extension = resume_file.name.split(".")[-1].lower()

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=f".{file_extension}"
            ) as tmp:
                tmp.write(resume_file.read())
                resume_path = tmp.name

            # Extract & preprocess
            resume_text = extract_text(resume_path)
            resume_clean = preprocess_text(resume_text)
            jd_clean = preprocess_text(jd_text)

            # Keywords
            resume_keywords = extract_keywords(resume_clean)
            jd_keywords = extract_keywords(jd_clean)

            # Match score
            score = calculate_match_score(resume_clean, jd_clean)

            # Compare keywords
            matched, missing, extra = compare_keywords(
                resume_keywords, jd_keywords
            )

            os.remove(resume_path)

            # Display results
            st.subheader(f"✅ Match Score: {score}%")

            st.markdown("### 🟢 Matched Keywords")
            st.write(matched if matched else "No strong matches found")

            st.markdown("### 🔴 Missing Keywords (Improve Resume)")
            st.write(missing if missing else "None")

            st.markdown("### 🔵 Extra Resume Keywords")
            st.write(extra if extra else "None")

        except ValueError:
            st.error(
                "❌ Unsupported file format. "
                "Please upload a valid PDF or DOCX resume."
            )

        except Exception:
            st.error(
                "⚠️ Something went wrong while processing the resume. "
                "Please try again with a different file."
            )

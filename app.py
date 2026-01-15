from extractor import extract_text
from preprocess import preprocess_text
from keywords import extract_keywords

# Load data
resume_text = extract_text("sample_data/resume.pdf")
with open("sample_data/jd.txt", "r", encoding="utf-8") as f:
    jd_text = f.read()

# Preprocess
resume_clean = preprocess_text(resume_text)
jd_clean = preprocess_text(jd_text)

# Extract keywords
resume_keywords = extract_keywords(resume_clean)
jd_keywords = extract_keywords(jd_clean)

print("Resume Keywords:")
print(resume_keywords)

print("\nJD Keywords:")
print(jd_keywords)

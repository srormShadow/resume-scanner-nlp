from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from keywords import extract_keywords
from skill_groups import SKILL_GROUPS
import re

def calculate_match_score(resume_text, jd_text):
    if not resume_text.strip() or not jd_text.strip():
        return 0.0

    vectorizer = TfidfVectorizer()

    try:
        vectors = vectorizer.fit_transform([resume_text, jd_text])
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])
        return round(similarity[0][0] * 100, 2)
    except ValueError:
        return 0.0

def compare_keywords(resume_keywords, jd_keywords):
    resume_set = normalize_keywords(resume_keywords)
    jd_set = normalize_keywords(jd_keywords)

    matched = list(resume_set & jd_set)
    missing = list(jd_set - resume_set)
    extra = list(resume_set - jd_set)

    return matched, missing, extra

def normalize_keywords(keywords):
    normalized = set(keywords)

    for group in SKILL_GROUPS.values():
        if any(skill in normalized for skill in group):
            normalized.update(group)

    return normalized

def split_sections(text):
    sections = {
        "skills": "",
        "experience": "",
        "tools": ""
    }

    text = text.lower()

    if "skills" in text:
        sections["skills"] = text.split("skills", 1)[1][:500]

    if "experience" in text:
        sections["experience"] = text.split("experience", 1)[1][:1000]

    if "tools" in text or "technologies" in text:
        key = "tools" if "tools" in text else "technologies"
        sections["tools"] = text.split(key, 1)[1][:500]

    return sections

def section_similarity(section_text, jd_text):
    # Guard against empty or useless text
    if not section_text or not section_text.strip():
        return 0.0

    if not jd_text or not jd_text.strip():
        return 0.0

    vectorizer = TfidfVectorizer()

    try:
        vectors = vectorizer.fit_transform([section_text, jd_text])
        return cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    except ValueError:
        # Handles empty vocabulary edge cases
        return 0.0

def calculate_section_based_score(resume_text, jd_text):
    sections = split_sections(resume_text)

    skill_score = section_similarity(sections["skills"], jd_text)
    exp_score = section_similarity(sections["experience"], jd_text)
    tool_score = section_similarity(sections["tools"], jd_text)

    final_score = (
        0.5 * skill_score +
        0.3 * exp_score +
        0.2 * tool_score
    )

    return {
        "skills": round(skill_score * 100, 2),
        "experience": round(exp_score * 100, 2),
        "tools": round(tool_score * 100, 2),
        "overall": round(final_score * 100, 2)
    }

def missing_keywords_by_section(resume_text, jd_text):
    sections = split_sections(resume_text)

    jd_keywords = set(extract_keywords(jd_text))

    results = {}

    for section, text in sections.items():
        section_keywords = set(extract_keywords(text))
        missing = list(jd_keywords - section_keywords)
        results[section] = missing

    return results

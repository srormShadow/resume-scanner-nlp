from sklearn.feature_extraction.text import TfidfVectorizer

def extract_keywords(text, top_n=20):
    if not text or not text.strip():
        return []

    vectorizer = TfidfVectorizer(max_features=top_n)

    try:
        vectorizer.fit_transform([text])
        return list(vectorizer.get_feature_names_out())
    except ValueError:
        return []


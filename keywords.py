from sklearn.feature_extraction.text import TfidfVectorizer

def extract_keywords(text, top_n=20):
    vectorizer = TfidfVectorizer(max_features=top_n)
    tfidf_matrix = vectorizer.fit_transform([text])
    keywords = vectorizer.get_feature_names_out()
    return list(keywords)

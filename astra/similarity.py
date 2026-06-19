from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def sentence_similarity(sentence1, sentence2):
    """
    Returns similarity score between two sentences.
    """

    documents = [sentence1, sentence2]

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )

    return float(similarity[0][0])


def find_most_similar(question, knowledge):
    """
    Find the most similar sentence from knowledge.
    Returns:
        (best_sentence, similarity_score)
    """

    if not knowledge:
        return None, 0

    documents = knowledge + [question]

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(
        documents
    )

    similarities = cosine_similarity(
        tfidf_matrix[-1],
        tfidf_matrix[:-1]
    )[0]

    best_index = similarities.argmax()

    best_score = similarities[best_index]

    return (
        knowledge[best_index],
        float(best_score)
    )
    
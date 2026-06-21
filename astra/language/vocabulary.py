from astra.language.keywords import extract_keywords


def build_vocabulary_from_text(text, max_words=20):

    return extract_keywords(
        text,
        max_words
    )

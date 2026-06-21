import re
from collections import Counter

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "can",
    "for",
    "from",
    "has",
    "have",
    "how",
    "in",
    "into",
    "is",
    "it",
    "its",
    "known",
    "of",
    "on",
    "or",
    "that",
    "the",
    "their",
    "this",
    "to",
    "very",
    "was",
    "were",
    "what",
    "when",
    "where",
    "which",
    "who",
    "why",
    "with"
}


def extract_keywords(text, max_keywords=12):

    words = re.findall(
        r"\b[a-zA-Z][a-zA-Z-]{2,}\b",
        text.lower()
    )

    meaningful_words = [
        word
        for word in words
        if word not in STOP_WORDS
    ]

    counts = Counter(meaningful_words)

    return [
        word
        for word, count in counts.most_common(max_keywords)
    ]

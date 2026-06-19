import numpy as np
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()

import re

def tokenize(sentence):
    return re.findall(
        r"\b\w+\b",
        sentence.lower()
    )

def stem(word):
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, vocabulary):

    tokenized_sentence = [
        stem(word)
        for word in tokenized_sentence
    ]

    bag = np.zeros(
        len(vocabulary),
        dtype=np.float32
    )

    for idx, word in enumerate(vocabulary):
        if word in tokenized_sentence:
            bag[idx] = 1

    return bag
import json
import os

from astra.similarity import sentence_similarity

FILE = "knowledge.json"


def load_knowledge():
    """
    Load all learned sentences.
    """

    if not os.path.exists(FILE):
        return []

    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_knowledge(data):
    """
    Save knowledge to disk.
    """

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


def learn_sentence(sentence):
    """
    Store a new sentence if it doesn't already exist.
    """

    sentence = sentence.strip()

    if not sentence:
        return False

    knowledge = load_knowledge()

    if sentence not in knowledge:
        knowledge.append(sentence)
        save_knowledge(knowledge)
        return True

    return False


from astra.similarity import find_most_similar  


def find_best_match(question):

    knowledge = load_knowledge()

    if not knowledge:
        return None

    best_sentence, score = find_most_similar(
        question,
        knowledge
    )

    if score < 0.25:
        return None

    return best_sentence


def get_all_knowledge():
    """
    Return all learned knowledge.
    """

    return load_knowledge()


def clear_knowledge():
    """
    Delete all learned knowledge.
    """

    save_knowledge([])
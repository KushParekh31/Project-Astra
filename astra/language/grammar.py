import random
import re


def sentence_case(text):

    text = text.strip()

    if not text:
        return text

    return text[0].upper() + text[1:]


def ensure_period(text):

    text = text.strip()

    if not text:
        return text

    if text[-1] in ".!?":
        return text

    return text + "."


def clean_sentence(text):

    return ensure_period(
        sentence_case(text)
    )


def reply_from_fact(fact):

    fact = clean_sentence(fact)

    templates = [
        "{fact}",
        "I know this: {fact}",
        "From what I have learned, {fact}",
        "A good way to say it is: {fact}",
        "Here is what I remember: {fact}"
    ]

    return random.choice(templates).format(
        fact=fact
    )


def reply_from_keywords(topic, keywords):

    topic = clean_topic(topic)

    if not keywords:
        return (
            f"I know about {topic}, but I do not have "
            "strong keywords saved yet."
        )

    keyword_text = ", ".join(
        keywords[:6]
    )

    templates = [
        "{topic} is mainly about {keywords}.",
        "I have learned that {topic} relates to {keywords}.",
        "The important ideas in {topic} are {keywords}.",
        "For {topic}, I remember these key ideas: {keywords}.",
        "{topic} connects most strongly to {keywords}."
    ]

    return random.choice(templates).format(
        topic=topic,
        keywords=keyword_text
    )


def clean_topic(topic):

    topic = topic.strip()

    if not topic:
        return topic

    return sentence_case(topic)


def extract_topic_from_question(text):

    text = text.strip()

    patterns = [
        r"^(tell me about|tell me|explain|describe|what is|who is|what are|define)\s+",
        r"\?$"
    ]

    topic = text

    for pattern in patterns:
        topic = re.sub(
            pattern,
            "",
            topic,
            flags=re.IGNORECASE
        ).strip()

    return topic or text

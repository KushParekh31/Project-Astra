import random


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

    if not keywords:
        return (
            f"I know about {topic}, but I do not have "
            "strong keywords saved yet."
        )

    keyword_text = ", ".join(
        keywords[:8]
    )

    templates = [
        "{topic} is connected with {keywords}.",
        "When I think about {topic}, the main ideas are {keywords}.",
        "The key points I learned about {topic} are {keywords}.",
        "My notes for {topic} focus on {keywords}.",
        "{topic} mainly relates to {keywords}."
    ]

    return random.choice(templates).format(
        topic=topic,
        keywords=keyword_text
    )

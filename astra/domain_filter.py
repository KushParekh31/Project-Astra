import json


DOMAINS_FILE = "data/domains.json"


def load_domains():

    with open(
        DOMAINS_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


import re


def score_topic(
    topic,
    domain="programming"
):

    domains = load_domains()

    keywords = domains.get(
        domain,
        []
    )

    words = set(
        re.findall(
            r"\b\w+\b",
            topic.lower()
        )
    )

    score = 0

    for keyword in keywords:

        if keyword.lower() in words:

            score += 1

    return score


def is_allowed(
    topic,
    domain="programming",
    min_score=1
):

    return (
        score_topic(
            topic,
            domain
        ) >= min_score
    )
    

def score_summary(
    summary,
    domain="programming"
):

    domains = load_domains()

    keywords = domains.get(
        domain,
        []
    )

    words = set(
        re.findall(
            r"\b\w+\b",
            summary.lower()
        )
    )

    score = 0

    for keyword in keywords:

        if keyword.lower() in words:

            score += 1

    return score

def calculate_relevance(
    topic,
    summary,
    domain="programming"
):

    title_score = score_topic(
        topic,
        domain
    )

    summary_score = score_summary(
        summary,
        domain
    )

    return (
        title_score +
        summary_score
    )
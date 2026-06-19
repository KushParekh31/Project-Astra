from astra.wiki_research import get_summary
from astra.domain_filter import *

topics = [
    "CPython",
    "Guido van Rossum",
    "Pythonidae",
    "Python (missile)"
]

for topic in topics:

    summary = get_summary(topic)

    score = calculate_relevance(
        topic,
        summary
    )

    print()
    print(topic)
    print("Score:", score)
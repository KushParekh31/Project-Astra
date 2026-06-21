from astra.curiosity.engine import *
from astra.curiosity.wiki_research import *

topic = input(
    "Starting Topic: "
).strip()

clear_queue()
clear_visited()

add_topic(topic)

while True:

    queue = get_queue()

    if not queue:

        print(
            "Research complete."
        )

        break

    topic = queue.pop(0)

    save_queue(queue)

    print()
    print("=" * 60)
    print("Researching:", topic)

    summary = get_summary(topic)

    if not summary:

        continue

    related = get_related_topics(
        topic
    )

    add_node(
        topic,
        summary,
        related
    )

    added = enqueue_related_topics(
    related
    )
    
    print(
    f"Accepted: {added}"
    )

    print(
        f"Rejected: {len(related) - added}"
    )

    print(
        f"Queued {added} new topics."
    )
    
    mark_visited(topic)

    print(
        "Saved:",
        topic
    )

    print(
        "Related Topics:",
        len(related)
    )

    break

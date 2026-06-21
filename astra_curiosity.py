from astra.curiosity.engine import research_topic_loop
from astra.curiosity.wiki_research import get_related_topics, get_summary


topic = input(
    "Starting Topic: "
).strip()

limit_text = input(
    "Max topics to learn this run [10]: "
).strip()

max_topics = int(limit_text) if limit_text else 10

delay_text = input(
    "Delay seconds between topics [2]: "
).strip()

delay_seconds = int(delay_text) if delay_text else 2

result = research_topic_loop(
    topic=topic,
    get_summary=get_summary,
    get_related_topics=get_related_topics,
    reset=True,
    max_topics=max_topics,
    delay_seconds=delay_seconds
)

print()
print("=" * 60)
print(result["message"])
print("Starting Topic:", result["start_topic"])
print("Processed:", result["processed"])
print("Remaining Queue:", result["remaining_queue"])

for item in result["results"]:
    print()
    print("Saved:", item["topic"])
    print("Accepted:", item["accepted"])
    print("Rejected:", item["rejected"])
    print("Related Topics:", len(item["related"]))

import json
import os
import time

from astra.curiosity.domain_filter import is_allowed
from astra.core.similarity import find_most_similar
from astra.language.keywords import extract_keywords

QUEUE_FILE = "data/curiosity/queue.json"
VISITED_FILE = "data/curiosity/visited.json"
RESEARCH_LOG_FILE = "data/curiosity/research_log.json"


def load_json(path, default):

    if not os.path.exists(path):
        return default

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


def get_queue():

    return load_json(
        QUEUE_FILE,
        []
    )


def save_queue(queue):

    save_json(
        QUEUE_FILE,
        queue
    )


def get_visited():

    return load_json(
        VISITED_FILE,
        []
    )


def save_visited(visited):

    save_json(
        VISITED_FILE,
        visited
    )


def add_topic(topic):

    queue = get_queue()

    if topic not in queue:
        queue.append(topic)

    save_queue(queue)
    
GRAPH_FILE = "data/curiosity/graph.json"


def get_graph():

    return load_json(
        GRAPH_FILE,
        {}
    )


def save_graph(graph):

    save_json(
        GRAPH_FILE,
        graph
    )


def add_node(
    topic,
    summary,
    related,
    keywords=None
):

    graph = get_graph()

    graph[topic] = {
        "keywords": keywords or extract_keywords(summary),
        "related": related
    }

    save_graph(graph)


def get_research_log():

    return load_json(
        RESEARCH_LOG_FILE,
        []
    )


def save_research_log(log):

    save_json(
        RESEARCH_LOG_FILE,
        log
    )


def add_research_log_entry(entry):

    log = get_research_log()

    log.append(entry)

    save_research_log(log)
    
def mark_visited(topic):

    visited = get_visited()

    if topic not in visited:

        visited.append(topic)

        save_visited(visited)
        
def enqueue_related_topics(
    topics,
    domain="programming",
    min_score=1
):

    queue = get_queue()

    visited = get_visited()

    added = 0

    for topic in topics:

        if not is_allowed(
            topic,
            topic,
            domain,
            min_score
        ):
            continue

        if topic in queue:
            continue

        if topic in visited:
            continue

        queue.append(topic)

        added += 1

    save_queue(queue)

    return added

def clear_queue():

    save_queue([])


def clear_visited():

    save_visited([])


def research_topic(
    topic,
    get_summary,
    get_related_topics,
    domain="programming",
    reset=False
):

    topic = topic.strip()

    if not topic:
        raise ValueError("Topic cannot be empty.")

    if reset:
        clear_queue()
        clear_visited()

    add_topic(topic)

    queue = get_queue()

    if topic in queue:
        queue.remove(topic)

    save_queue(queue)

    summary = get_summary(topic)

    if not summary:
        return {
            "topic": topic,
            "saved": False,
            "related": [],
            "accepted": 0,
            "rejected": 0,
            "message": "No summary found."
        }

    related = get_related_topics(topic)
    keywords = extract_keywords(summary)

    add_node(
        topic,
        summary,
        related,
        keywords
    )

    accepted = enqueue_related_topics(
        related,
        domain
    )

    mark_visited(topic)

    rejected = len(related) - accepted

    result = {
        "topic": topic,
        "saved": True,
        "keywords": keywords,
        "related": related,
        "accepted": accepted,
        "rejected": rejected,
        "message": f"Saved research for {topic}."
    }

    add_research_log_entry(result)

    return result


def research_topic_loop(
    topic,
    get_summary,
    get_related_topics,
    domain="programming",
    reset=False,
    max_topics=10,
    delay_seconds=2,
    progress_callback=None,
    should_stop=None
):

    topic = topic.strip()

    if not topic:
        raise ValueError("Topic cannot be empty.")

    if reset:
        clear_queue()
        clear_visited()

    add_topic(topic)

    results = []
    processed = 0

    while True:

        if should_stop and should_stop():
            break

        if max_topics and processed >= max_topics:
            break

        queue = get_queue()

        if not queue:
            break

        current_topic = queue.pop(0)

        save_queue(queue)

        visited = get_visited()

        if current_topic in visited:
            continue

        result = research_topic(
            topic=current_topic,
            get_summary=get_summary,
            get_related_topics=get_related_topics,
            domain=domain,
            reset=False
        )

        results.append(result)
        processed += 1

        if progress_callback:
            progress_callback(result, processed)

        if delay_seconds:
            time.sleep(delay_seconds)

    return {
        "start_topic": topic,
        "processed": processed,
        "results": results,
        "remaining_queue": len(get_queue()),
        "message": (
            f"Research loop complete. "
            f"Processed {processed} topic(s)."
        )
    }
    
def find_topic(query):

    graph = get_graph()

    if not graph:
        return None

    topics = list(
        graph.keys()
    )

    best_topic, score = (
        find_most_similar(
            query,
            topics
        )
    )

    print(
        f"[DEBUG] "
        f"Best Topic: {best_topic}"
    )

    print(
        f"[DEBUG] "
        f"Score: {score:.3f}"
    )

    if score < 0.15:
        return None

    return graph[best_topic]


def find_topic_keywords(query):

    topic_data = find_topic(query)

    if not topic_data:
        return None

    return {
        "keywords": topic_data.get("keywords", [])
    }

import json
import os

from astra.domain_filter import is_allowed
from astra.similarity import find_most_similar

QUEUE_FILE = "data/curiosity/queue.json"
VISITED_FILE = "data/curiosity/visited.json"


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
    related
):

    graph = get_graph()

    graph[topic] = {
        "summary": summary,
        "related": related
    }

    save_graph(graph)
    
def mark_visited(topic):

    visited = get_visited()

    if topic not in visited:

        visited.append(topic)

        save_visited(visited)
        
def enqueue_related_topics(
    topics,
    domain="programming"
):

    queue = get_queue()

    visited = get_visited()

    added = 0

    for topic in topics:

        if not is_allowed(
            topic,
            domain
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
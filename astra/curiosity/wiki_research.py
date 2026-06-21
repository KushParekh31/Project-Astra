import time

import requests

HEADERS = {
    "User-Agent":
    "Project-Astra/0.1 (Research Bot; Python)"
}

DEFAULT_TIMEOUT = 10
MAX_RETRIES = 3


def _sleep_before_retry(response, attempt):

    retry_after = response.headers.get(
        "Retry-After"
    )

    if retry_after and retry_after.isdigit():
        time.sleep(
            int(retry_after)
        )
        return

    time.sleep(
        attempt + 1
    )


def _get_json(url, params=None):

    for attempt in range(MAX_RETRIES):

        response = requests.get(
            url,
            headers=HEADERS,
            params=params,
            timeout=DEFAULT_TIMEOUT
        )

        print("Status:", response.status_code)

        if response.status_code == 429:
            print(
                "Rate limited by Wikipedia. "
                "Waiting before retry..."
            )
            _sleep_before_retry(
                response,
                attempt
            )
            continue

        if not response.ok:
            print(
                f"Wikipedia request failed: "
                f"{response.status_code}"
            )
            return None

        try:
            return response.json()
        except ValueError:
            print(
                "Wikipedia returned a non-JSON response."
            )
            return None

    print(
        "Wikipedia rate limit persisted. "
        "Try again later or use fewer topics."
    )

    return None


def get_summary(topic):

    try:

        url = (
            "https://en.wikipedia.org/api/rest_v1/page/summary/"
            + topic.replace(" ", "_")
        )

        data = _get_json(url)

        if not data:
            return None

        return data.get(
            "extract",
            "No summary found."
        )

    except Exception as e:

        print(
            f"Summary Error: {e}"
        )

        return None
    
def get_related_topics(topic):

    try:

        url = (
            "https://en.wikipedia.org/w/api.php"
        )

        params = {
            "action": "query",
            "titles": topic,
            "prop": "links",
            "pllimit": 50,
            "format": "json"
        }

        data = _get_json(
            url,
            params=params
        )

        if not data:
            return []

        pages = data["query"]["pages"]

        links = []

        for page_id in pages:

            page = pages[page_id]

            if "links" in page:

                for link in page["links"]:

                    links.append(
                        link["title"]
                    )

        return links

    except Exception as e:

        print(
            f"Links Error: {e}"
        )

        return []

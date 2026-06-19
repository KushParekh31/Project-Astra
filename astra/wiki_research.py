import requests

HEADERS = {
    "User-Agent":
    "Project-Astra/0.1 (Research Bot; Python)"
}


def get_summary(topic):

    try:

        url = (
            "https://en.wikipedia.org/api/rest_v1/page/summary/"
            + topic.replace(" ", "_")
        )

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        print("Status:", response.status_code)

        data = response.json()

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

        response = requests.get(
            url,
            headers=HEADERS,
            params=params,
            timeout=10
        )

        data = response.json()

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
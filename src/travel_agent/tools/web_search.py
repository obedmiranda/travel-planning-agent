import os

import serpapi
from dotenv import load_dotenv

from travel_agent.models.search_result import SearchResult

load_dotenv()


def web_search(query: str) -> list[SearchResult]:
    client = serpapi.Client(api_key=os.getenv("SERPAPI_KEY"))

    results = client.search(
        {
            "engine": "google",
            "q": query,
        }
    )

    organic_results = results["organic_results"]
    search_results: list[SearchResult] = []

    for result in organic_results:
        search_result = SearchResult(
            title=result["title"],
            url=result["link"],
            snippet=result["snippet"],
        )

        search_results.append(search_result)

    return search_results


if __name__ == "__main__":
    results = web_search("Japan Rail Pass Tokyo Kyoto Osaka")
    print(results)

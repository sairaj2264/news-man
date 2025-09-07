import os
from tavily import TavilyClient

class NewsService:
    """
    A service to handle fetching news articles using the Tavily API.
    """
    def __init__(self):
        # Initialize the Tavily client with the API key from environment variables
        self.tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

    def fetch_raw_articles(self, topic: str, max_results: int = 5):
        """
        Fetches raw article data from Tavily based on a topic.

        :param topic: The topic to search for (e.g., "technology").
        :param max_results: The maximum number of articles to fetch.
        :return: A list of raw article data or an error dictionary.
        """
        try:
            # Construct a search query for Tavily
            query = f"latest top {max_results} news articles about {topic}"

            # Perform an advanced search to get the full content of the articles
            response = self.tavily_client.search(
                query=query,
                search_depth="advanced",
                max_results=max_results,
                include_raw_content=True # Ensure we get the full text
            )

            # The search results are in the 'results' key
            return response['results']

        except Exception as e:
            # In a real app, you would log this error
            print(f"An error occurred while fetching from Tavily: {e}")
            return {"error": "Failed to fetch articles from the provider."}, 500

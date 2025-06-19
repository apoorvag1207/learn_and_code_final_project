from server.services.news_service import NewsService

class PeriodicNewsFetcher:
    def __init__(self):
        self.service = NewsService()

    def run_once(self):
        self.service.fetch_and_store_all_news()

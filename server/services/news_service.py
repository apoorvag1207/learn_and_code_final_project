from utils.external_news_fetcher import ExternalNewsFetcher
from services.news_storage_service import NewsStorageService

class NewsService:
    def __init__(self):
        self.fetcher = ExternalNewsFetcher()
        self.storage = NewsStorageService()

    def fetch_and_store_all_news(self):
        print("[NewsService] Fetching news from all sources...")
        articles = self.fetcher.get_all_news()
        print(f"[NewsService] Total articles fetched: {len(articles)}")

        success = 0
        for article in articles:
            try:
                self.storage.save_article(article)
                success += 1
            except Exception as e:
                print(f"[NewsService] Error saving article: {e}")

        print(f"[NewsService] Successfully stored {success} articles.")

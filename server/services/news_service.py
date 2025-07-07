from utils.external_news_fetcher import ExternalNewsFetcher
from services.news_storage_service import NewsStorageService
from db_connection import DatabaseConnector

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
        
    def notify_users_for_article(self, article):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            title = article['title']
            message = article['description']
            category = article['category']
            cursor.execute("""
                SELECT UserId FROM NotificationConfiguration
                WHERE Category = %s AND isEnabled = 1 AND ReceiveEmails = 1
            """, (category,))
            category_users = cursor.fetchall()

            for user in category_users:
                self.notification_service.notify_user(user['UserId'], title, message)
            cursor.execute("SELECT DISTINCT UserId, Word FROM Keyword")
            keyword_users = cursor.fetchall()
            for row in keyword_users:
                if row["Word"].lower() in (title + message).lower():
                    self.notification_service.notify_user(row['UserId'], title, message)

        except Exception as e:
            print(f"[ERROR] notify_users_for_article failed: {e}")
        finally:
            cursor.close()
            conn.close()

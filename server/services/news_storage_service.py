from db_connection import DatabaseConnector
from datetime import datetime, timedelta
from utils.category_inferer import CategoryInferer
from services.notification_service import NotificationService


class NewsStorageService:
    def __init__(self):
        self.db = DatabaseConnector()
        self.category_inferer = CategoryInferer()
        self.notifier = NotificationService()
    
    def save_article(self, article):
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)

            title = article.get("title")
            description = article.get("description")
            content = article.get("content")
            url = article.get("url")
            published_at = self.parse_datetime(article.get("publishedAt") or article.get("published_at"))
            source = self.extract_source(article.get("source"))

            if "category" in article:
                category = article.get("category", "general").lower()
            elif "categories" in article:
                category = article["categories"][0].lower() if article["categories"] else "general"
            else:
                category = self.category_inferer.infer_category(title, description)

            cursor.execute("SELECT COUNT(*) FROM NewsArticle WHERE title = %s AND source = %s", (title, source))
            if cursor.fetchone()["COUNT(*)"] > 0:
                return

            insert_query = """
                INSERT INTO NewsArticle (Title, Description, Content, URL, PublishedAt, Source, Category)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (title, description, content, url, published_at, source, category))
            conn.commit()

            cursor.execute("SELECT LAST_INSERT_ID() AS id")
            article_id = cursor.fetchone()["id"]

            matched_user_ids = self.notifier.get_users_to_notify(category, title + " " + (description or ""))
            for user_id in matched_user_ids:
                self.notifier.notify_user(
                    user_id=user_id,
                    article_id=article_id,
                    title=title,
                    message=f"\n\n{title}\n\n{description}\n\nRead more: {url}"
                )

        except Exception as e:
            print(f" Error saving article: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def bulk_store_articles(self, articles):
        for article in articles:
            try:
                self.save_article(article)
            except Exception as e:
                print(f"[StorageService] Skipping article due to error: {e}")

    def parse_datetime(self, datetime_str):
        if not datetime_str:
            return None
        try:
            date = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            try:
                date = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")
            except:
                return None
        return date + timedelta(hours=5, minutes=30)

    def extract_source(self, source):
        if isinstance(source, dict):
            return source.get("name", "Unknown")
        return source or "Unknown"

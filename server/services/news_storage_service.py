from db_connection import DatabaseConnector
from datetime import datetime, timedelta
from utils.category_inferer import CategoryInferer

class NewsStorageService:
    def __init__(self):
        self.db = DatabaseConnector()
        self.category_inferer = CategoryInferer()

    def save_article(self, article):
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

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
            if cursor.fetchone()[0] > 0:
                return

            insert_query = """
                INSERT INTO NewsArticle (Title, Description, Content, URL, PublishedAt, Source, Category)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE title = VALUES(title)
            """
            cursor.execute(insert_query, (title, description, content, url, published_at, source, category))
            conn.commit()

        except Exception as e:
            print(f"[NewsService] Error saving article: {e}")
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

from db_connection import DatabaseConnector

class UserHeadlineService:
    def __init__(self):
        self.db = DatabaseConnector()

    def get_articles_by_date(self, date, category):
        print(f" get_articles_by_date() called with date: {date}, category: {category}")

        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT 
                NewsArticle.NewsArticleId AS id,
                NewsArticle.Title AS title,
                NewsArticle.Description AS description,
                NewsArticle.Source AS source,
                NewsArticle.URL AS url,
                NewsArticle.PublishedAt AS published_at,
                NewsArticle.Category AS category
            FROM NewsArticle
            WHERE DATE(NewsArticle.PublishedAt) = %s
        """
        params = [date]

        if category.lower() != "all":
            query += " AND LOWER(NewsArticle.Category) = %s"
            params.append(category.lower())

        print(f"Final SQL Query: {query}")
        print(f"Parameters: {params}")

        cursor.execute(query, params)
        results = cursor.fetchall()

        print(f"Number of articles fetched: {len(results)}")
        for result in results:
            print(f"Article ID: {result['id']}, PublishedAt: {result['published_at']}")

        cursor.close()
        connection.close()
        return results

    def get_articles_by_date_range(self, start_date, end_date, category):
        print(f"get_articles_by_date_range() called with start: {start_date}, end: {end_date}, category: {category}")

        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT 
                NewsArticle.NewsArticleId AS id,
                NewsArticle.Title AS title,
                NewsArticle.Description AS description,
                NewsArticle.Source AS source,
                NewsArticle.URL AS url,
                NewsArticle.PublishedAt AS published_at,
                NewsArticle.Category AS category
            FROM NewsArticle
            WHERE DATE(NewsArticle.PublishedAt) BETWEEN %s AND %s
        """
        params = [start_date, end_date]

        if category.lower() != "all":
            query += " AND LOWER(NewsArticle.Category) = %s"
            params.append(category.lower())
        cursor.execute(query, params)
        results = cursor.fetchall()

        print(f" Number of articles fetched: {len(results)}")
        for result in results:
            print(f" Article ID: {result['id']}, PublishedAt: {result['published_at']}")

        cursor.close()
        connection.close()
        return results

    def get_saved_articles(self, user_id):
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT 
                SavedArticle.SavedArticleId AS id,
                NewsArticle.Title AS title,
                NewsArticle.Description AS description,
                NewsArticle.Source AS source,
                NewsArticle.URL AS url,
                NewsArticle.Category AS category,
                NewsArticle.PublishedAt AS published_at
            FROM SavedArticle
            JOIN NewsArticle ON SavedArticle.NewsArticleId = NewsArticle.NewsArticleId
            WHERE SavedArticle.UserId = %s
        """
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()

        cursor.close()
        connection.close()
        return results

    def delete_saved_article(self, user_id, article_id):
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM SavedArticle WHERE UserId = %s AND SavedArticleId = %s",
                (user_id, article_id)
            )
            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"[ERROR] Failed to delete saved article: {e}")
            return False
        finally:
            cursor.close()
            connection.close()

    def search_articles(self, search_query, start_date=None, end_date=None):
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            sql = """
                SELECT 
                    n.NewsArticleId AS id,
                    n.Title AS title,
                    n.Description AS description,
                    n.Source AS source,
                    n.URL AS url,
                    n.Category AS category,
                    n.PublishedAt AS published_at,
                    COALESCE(SUM(CASE WHEN af.IsLiked = 1 THEN 1 ELSE 0 END), 0) AS likes,
                    COALESCE(SUM(CASE WHEN af.IsLiked = 0 THEN 1 ELSE 0 END), 0) AS dislikes
                FROM NewsArticle n
                LEFT JOIN ArticleFeedback af ON n.NewsArticleId = af.NewsArticleId
                WHERE n.Title LIKE %s OR n.Description LIKE %s
            """
            params = [f"%{search_query}%", f"%{search_query}%"]

            if start_date and end_date:
                sql += " AND DATE(n.PublishedAt) BETWEEN %s AND %s"
                params.extend([start_date, end_date])

            sql += """
                GROUP BY n.NewsArticleId
                ORDER BY likes DESC, dislikes ASC, n.PublishedAt DESC
            """

            cursor.execute(sql, tuple(params))
            return cursor.fetchall()
        finally:
            cursor.close()
            connection.close()

            
    def give_article_feedback(self, user_id, article_id, is_liked):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO ArticleFeedback (UserId, NewsArticleId, IsLiked)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE IsLiked = VALUES(IsLiked), FeedbackAt = NOW()
            """, (user_id, article_id, is_liked))
            conn.commit()
            return True
        except Exception as e:
            print(f"[ERROR] Feedback failed: {e}")
            return False
        finally:
            cursor.close()
            conn.close()



from db_connection import DatabaseConnector

class UserHeadlineService:
    def __init__(self):
        self.db = DatabaseConnector()

    def get_articles_by_date(self, date, category):
        print(f"[DEBUG] get_articles_by_date() called with date: {date}, category: {category}")

        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                NewsArticleId AS id,
                Title AS title,
                Description AS description,
                Source AS source,
                URL AS url,
                PublishedAt AS publishedAt,
                Category AS category
            FROM NewsArticle
            WHERE DATE(PublishedAt) = %s
        """
        params = [date]

        if category.lower() != "all":
            query += " AND LOWER(Category) = %s"
            params.append(category.lower())

        print(f"[DEBUG] Final SQL Query: {query}")
        print(f"[DEBUG] Parameters: {params}")

        cursor.execute(query, params)
        results = cursor.fetchall()

        print(f"[DEBUG] Number of articles fetched: {len(results)}")
        for r in results:
            print(f"[DEBUG] Article ID: {r['id']}, PublishedAt: {r['publishedAt']}")

        cursor.close()
        conn.close()
        return results

    def get_articles_by_date_range(self, start, end, category):
        print(f"[DEBUG] get_articles_by_date_range() called with start: {start}, end: {end}, category: {category}")

        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                NewsArticleId AS id,
                Title AS title,
                Description AS description,
                Source AS source,
                URL AS url,
                PublishedAt AS publishedAt,
                Category AS category
            FROM NewsArticle
            WHERE DATE(PublishedAt) BETWEEN %s AND %s
        """
        params = [start, end]

        if category.lower() != "all":
            query += " AND LOWER(Category) = %s"
            params.append(category.lower())

        print(f"[DEBUG] Final SQL Query: {query}")
        print(f"[DEBUG] Parameters: {params}")

        cursor.execute(query, params)
        results = cursor.fetchall()

        print(f"[DEBUG] Number of articles fetched: {len(results)}")
        for r in results:
            print(f"[DEBUG] Article ID: {r['id']}, PublishedAt: {r['publishedAt']}")

        cursor.close()
        conn.close()
        return results
    
    def get_saved_articles(self, user_id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT sa.SavedArticleId AS id, na.Title AS title, na.Description AS description,
                   na.Source AS source, na.URL AS url, na.Category AS category, na.PublishedAt AS publishedAt
            FROM SavedArticle sa
            JOIN NewsArticle na ON sa.NewsArticleId = na.NewsArticleId
            WHERE sa.UserId = %s
        """
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def delete_saved_article(self, user_id, article_id):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM SavedArticle WHERE UserId = %s AND SavedArticleId = %s", (user_id, article_id))
            conn.commit()
            return cursor.rowcount > 0
        except:
            return False
        finally:
            cursor.close()
            conn.close()
    
    def search_articles(self, query):
        print(f"[DEBUG] search_articles() called with query: {query}")
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT 
                NewsArticleId AS id,
                Title AS title,
                Description AS description,
                Source AS source,
                URL AS url,
                PublishedAt AS publishedAt,
                Category AS category
            FROM NewsArticle
            WHERE Title LIKE %s OR Description LIKE %s
        """
        like_query = f"%{query}%"
        cursor.execute(sql, (like_query, like_query))
        results = cursor.fetchall()

        print(f"[DEBUG] Number of search results: {len(results)}")

        cursor.close()
        conn.close()
        return results



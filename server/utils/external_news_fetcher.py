from utils.external_api import NewsAPIClient, TheNewsAPIClient, FirebaseAPIClient
from db_connection import DatabaseConnector
from datetime import datetime

class ExternalNewsFetcher:
    def __init__(self):
        self.db = DatabaseConnector()

    def get_active_servers(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Name, ApiKey FROM ExternalServer WHERE IsActive = TRUE")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return {row[0]: row[1] for row in rows}

    def update_last_accessed(self, server_name):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE ExternalServer SET LastAccessed = %s WHERE Name = %s",
            (datetime.now(), server_name)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def get_all_news(self):
        news = []
        servers = self.get_active_servers()

        for name, api_key in servers.items():
            try:
                if name == "TheNewsAPI":
                    client = TheNewsAPIClient(api_key)
                elif name == "NewsAPI":
                    client = NewsAPIClient(api_key)
                elif name == "Firebase":
                    client = FirebaseAPIClient(api_key)
                else:
                    print(f"[Fetcher] Unknown server: {name}")
                    continue

                fetched = client.fetch_news()
                news.extend(fetched)
                self.update_last_accessed(name)
                print(f"[Fetcher] {name}: Fetched {len(fetched)} articles.")

            except Exception as e:
                print(f"[Fetcher] Error fetching from {name}: {e}")

        return news

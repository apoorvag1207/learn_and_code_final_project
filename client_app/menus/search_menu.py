from services.news_client import NewsClient
from datetime import datetime

class SearchMenu:
    def __init__(self, user_data):
        self.user_data = user_data

    def search(self):
        query = input("Enter search query: ")
        print(f"\nS E A R C H\nResults for \"{query}\"")

        articles = NewsClient().search_articles(query)
        if not articles:
            print("No results found.")
            return

        for article in articles:
            published_str = article.get('publishedAt')
            try:
                published_dt = datetime.strptime(published_str, "%Y-%m-%d %H:%M:%S")
                published_formatted = published_dt.strftime("%d-%b-%Y %I:%M %p")
            except:
                published_formatted = published_str

            print(f"\nArticle ID: {article.get('id')}")
            print(f"{article.get('title')}")
            print(f"{article.get('description')}")
            print(f"source : {article.get('source')}")
            print(f"URL: {article.get('url')}")
            print(f"{article.get('category').capitalize()}: {article.get('category')}")

        while True:
            print("\n1. Back\n2. Logout\n3. Save Article")
            action = input("Choose an option: ")
            if action == "1":
                return
            elif action == "2":
                print("Logging out...")
                exit()
            elif action == "3":
                article_id = input("Enter Article ID to save: ")
                success = NewsClient().save_article(self.user_data["user_id"], article_id)
                print("Article saved." if success else "Failed to save.")

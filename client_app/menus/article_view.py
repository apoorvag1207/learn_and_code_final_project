from datetime import datetime
from services.news_client import NewsClient

class ArticleViewMenu:
    def __init__(self, user_data):
        self.user_data = user_data

    def display_articles(self, date_input, category):
        print(f"\nH E A D L I N E S - {category}")
        articles = NewsClient().fetch_headlines(date_input, category)

        if not articles:
            print("No articles found.")
            return

        for article in articles:
            published_string = article.get('publishedAt')
            try:
                published_dt = datetime.strptime(published_string, "%Y-%m-%d %H:%M:%S")
                published_formatted = published_dt.strftime("%d-%b-%Y %I:%M %p")
            except Exception:
                published_formatted = published_string  

            print(f"\nArticle ID: {article.get('id')}")
            print(f"Title: {article.get('title')}")
            print(f"{article.get('description')}")
            print(f"Source: {article.get('source')}")
            print(f"URL: {article.get('url')}\n")

        while True:
            print("\n1. Back")
            print("2. Logout")
            print("3. Save Article")
            print("4. Like Article")
            print("5. Dislike Article")
            action = input("Choose an option: ").strip()

            if action == "1":
                return
            elif action == "2":
                print("Logging out...")
                exit()
            elif action == "3":
                article_id = input("Enter Article ID to save: ").strip()
                success = NewsClient().save_article(self.user_data["user_id"], article_id)
                print(" Article saved." if success else " Failed to save article.")
            elif action == "4":
                article_id = input("Enter Article ID to like: ").strip()
                success = NewsClient().submit_feedback(self.user_data["user_id"], article_id, True)
                print("You liked the article." if success else "Failed to like the article.")
            elif action == "5":
                article_id = input("Enter Article ID to dislike: ").strip()
                success = NewsClient().submit_feedback(self.user_data["user_id"], article_id, False)
                print("You disliked the article." if success else "Failed to dislike the article.")
            else:
                print("Invalid choice. Try again.")

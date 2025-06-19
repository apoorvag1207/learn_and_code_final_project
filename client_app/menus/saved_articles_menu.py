from services.news_client import NewsClient
from datetime import datetime

class SavedArticlesMenu:
    def __init__(self, user_data):
        self.user_data = user_data

    def show_saved_articles(self):
        articles = NewsClient().get_saved_articles(self.user_data["user_id"])
        print("\nS A V E D")

        if not articles:
            print("No saved articles.")
            return

        for article in articles:
            published_str = article.get("publishedAt")
            try:
                dt = datetime.strptime(published_str, "%Y-%m-%d %H:%M:%S")
                published_formatted = dt.strftime("%d-%b-%Y %I:%M %p")
            except:
                published_formatted = published_str

            print(f"\nArticle Id: {article.get('id')} {article.get('title')}")
            print(article.get("description"))
            print(f"Source : {article.get('source')}")
            print(f"URL:\n{article.get('url')}")
            print(f"Category: {article.get('category')}")

        while True:
            print("\n1. Back\n2. Logout\n3. Delete Article")
            choice = input("Choose an option: ")
            if choice == "1":
                return
            elif choice == "2":
                print("Logging out...")
                exit()
            elif choice == "3":
                article_id = input("Enter Article ID to delete: ")
                success = NewsClient().delete_saved_article(self.user_data["user_id"], article_id)
                print("Deleted successfully." if success else "Failed to delete, article doesnt exist.")
                return
            else:
                print("Invalid option.")

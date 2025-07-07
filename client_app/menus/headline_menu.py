from menus.article_view import ArticleViewMenu
from utils.session import SessionManager

class HeadlineMenu:
    def __init__(self, user_data):
        self.user_data = user_data

    def show_headline_menu(self):
        while True:
            print("\n1. Today\n2. Date Range\n3. Logout")
            choice = input("Choose an option: ")

            if choice == "1":
                today = SessionManager.get_today_date()
                ArticleViewMenu(self.user_data).display_articles(today, category="All")
            elif choice == "2":
                start = input("Enter start date (YYYY-MM-DD): ")
                end = input("Enter end date (YYYY-MM-DD): ")
                self.select_category(f"{start}|{end}")
            elif choice == "3":
                print("Logging out...")
                exit()
            else:
                print("Invalid option.")



    def select_category(self, date_input):
        print("\nPlease choose the category")
        print("1. All\n2. Business\n3. Entertainment\n4. Sports\n5. Technology")
        category_map = {
            "1": "All", "2": "Business", "3": "Entertainment", "4": "Sports", "5": "Technology"
        }
        choice = input("Enter choice: ")
        category = category_map.get(choice, "All")
        ArticleViewMenu(self.user_data).display_articles(date_input, category)

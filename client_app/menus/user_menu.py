from menus.headline_menu import HeadlineMenu
from utils.session import SessionManager
from menus.saved_articles_menu import SavedArticlesMenu
from menus.search_menu import SearchMenu
from menus.notification_menu import NotificationsMenu

class UserMenu:
    def __init__(self, user_data):
        self.user_data = user_data

    def show_user_menu(self):
        print(f"\nWelcome to the News Application, {self.user_data['name']}!")
        print(f"Date: {SessionManager.get_formatted_date_time()}")

        while True:
            print("\nPlease choose the options below")
            print("1. Headlines")
            print("2. Saved Articles")
            print("3. Search")
            print("4. Notifications")
            print("5. Logout")
            choice = input("Enter choice: ")

            if choice == "1":
                HeadlineMenu(self.user_data).show_headline_menu()
            elif choice == "2":
                SavedArticlesMenu(self.user_data).show_saved_articles()
            elif choice == "3":
                SearchMenu(self.user_data).search()
            elif choice == "4":
                NotificationsMenu(self.user_data).show_notifications_menu()
            elif choice == "5":
                print("Logging out...")
                break
            else:
                print(" not implemented yet.")

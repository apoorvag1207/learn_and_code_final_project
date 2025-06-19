from auth.login import LoginHandler
from auth.signup import SignUpHandler
from menus.user_menu import UserMenu
from menus.admin_menu import AdminMenu

class NewsAggregatorClientApp:
    def __init__(self):
        self.login_handler = LoginHandler()
        self.signup_handler = SignUpHandler()

    def show_main_menu(self):
        while True:
            print("\n Welcome to  News Aggregator ")
            print("1. Login")
            print("2. Sign Up")
            print("3. Exit")
            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.handle_login()
            elif choice == "2":
                self.signup_handler.register_user()
            elif choice == "3":
                print("Exiting application. Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")

    def handle_login(self):
        user_data = self.login_handler.authenticate_user()
        if user_data:
            role = user_data.get("role")
            name = user_data.get("name")

            
            if role == "Admin":
                AdminMenu(user_data).show_admin_menu()
            else:
                UserMenu(user_data).show_user_menu()

if __name__ == "__main__":
    app = NewsAggregatorClientApp()
    app.show_main_menu()

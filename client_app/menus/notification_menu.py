import requests
from utils.session import SessionManager
from menus.notification_config_menu import NotificationConfigMenu


class NotificationsMenu:
    def __init__(self, user_data):  
        self.user = user_data

    def show_notifications_menu(self):
        while True:
            print(f"\nWelcome to News Application, {self.user['name']}! ")
            print("N O T I F I C A T I O N S")
            print("1. View Notifications")
            print("2. Configure Notifications")
            print("3. Back")
            print("4. Logout")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_notifications()
            elif choice == "2":
                NotificationConfigMenu(self.user).configure()
            elif choice == "3":
                return
            elif choice == "4":
                print("Logging out...")
                from client_app.main import main_menu
                main_menu()
                return
            else:
                print("Invalid choice. Try again.")

    def view_notifications(self):
        try:
            response = requests.get(f"http://localhost:5000/user/notifications/{self.user['user_id']}")
            notifications = response.json().get("notifications", [])

            print("\nYour Notifications:")
            if not notifications:
                print("No notifications available.")
            else:
                for index, notification in enumerate(notifications, 1):
                    print(f"{index}. {notification['Title']} - {notification['Message']}")
                    print(f"   Link: {notification['URL']}")
                    

        except Exception as e:
            print(f"Error fetching notifications: {e}")

import requests

class AdminMenu:
    
    def __init__(self, user_data):
        self.user_data = user_data  
    def show_admin_menu(self):
        while True:
            print("\nAdmin Menu")
            print("1. View list of external servers and status")
            print("2. View external server details")
            print("3. Update/Edit external server API key")
            print("4. Add new News Category")
            print("5. Logout")
            choice = input("Choose an option: ")

            if choice == "1":
                self.view_server_status()
            elif choice == "2":
                self.view_server_details()
            elif choice == "3":
                self.update_server_key()
            elif choice == "4":
                self.add_category()
            elif choice == "5":
                print("Logging out...")
                break
            else:
                print("Invalid choice")

    def view_server_status(self):
        response = requests.get("http://localhost:5000/admin/servers/status")
        for s in response.json():
            print(f"{s['Name']} - {'Active' if s['IsActive'] else 'Not Active'} - Last accessed: {s['LastAccessed']}")

    def view_server_details(self):
        response = requests.get("http://localhost:5000/admin/servers/details")
        for s in response.json():
            print(f"{s['ServerId']}. {s['Name']} - {s['ApiKey']}")

    def update_server_key(self):
        server_id = input("Enter server ID: ")
        new_key = input("Enter updated API key: ")
        requests.patch("http://localhost:5000/admin/servers/update", json={
            "server_id": server_id,
            "new_key": new_key
        })
        print("Updated successfully!")

    def add_category(self):
        print(" not implemented yet.")

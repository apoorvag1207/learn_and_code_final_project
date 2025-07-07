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
        for server in response.json():
            print(f"{server['Name']} - {'Active' if server['IsActive'] else 'Not Active'} - Last accessed: {server['LastAccessed']}")

    def view_server_details(self):
        response = requests.get("http://localhost:5000/admin/servers/details")
        for server in response.json():
            print(f"{server['ServerId']}. {server['Name']} - {server['ApiKey']}")

    def update_server_key(self):
        server_id = input("Enter server ID: ")
        new_key = input("Enter updated API key: ")
        requests.patch("http://localhost:5000/admin/servers/update", json={
            "server_id": server_id,
            "new_key": new_key
        })
        print("Updated successfully!")

    def add_category(self):
        category_name = input("Enter new category name: ").strip()
        if not category_name:
            print("Category name cannot be empty.")
            return

        try:
            response = requests.post(
                "http://localhost:5000/admin/categories",
                json={
                    "name": category_name,
                    "admin_id": self.user_data["user_id"]
                }
            )
            if response.status_code == 200:
                print("Category added successfully.")
            else:
                print("Failed to add category:", response.json().get("error", "Unknown error"))
        except Exception as e:
            print(f"Error: {e}")


from flask import Blueprint, request, jsonify
from services.notification_service import NotificationService

notification_routes = Blueprint('notification_routes', __name__)
service = NotificationService()

@notification_routes.route("/user/notifications/<int:user_id>", methods=["GET"])
def get_notifications(user_id):
    try:
        notifications = service.get_notifications(user_id)
        return jsonify({"notifications": notifications})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@notification_routes.route("/user/notification-config/<int:user_id>", methods=["GET"])
def get_notification_config(user_id):
    try:
        data = service.get_notification_config(user_id)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@notification_routes.route("/user/notification-config/update-status", methods=["PATCH"])
def update_notification_status():
    try:
        data = request.get_json()
        user_id = data["user_id"]
        config_id = data["config_id"]
        new_status = data["is_enabled"]
        service.update_notification_status(user_id, config_id, new_status)
        return jsonify({"message": "Notification setting updated successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@notification_routes.route("/user/keywords", methods=["POST"])
def set_keywords():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        keywords = data.get("keywords")

        if not user_id or not isinstance(keywords, list):
            return jsonify({"error": "Invalid input: user_id or keywords missing or invalid."}), 400

        service = NotificationService()
        service.set_keywords(user_id, keywords)
        return jsonify({"message": "Keywords updated successfully."}), 200

    except Exception as e:
        print(f"[ERROR] Failed to update keywords: {e}")
        return jsonify({"error": str(e)}), 500


@notification_routes.route("/user/notification-config/toggle/<int:user_id>/<int:config_id>", methods=["PATCH"])
def toggle_notification(user_id, config_id):
    try:
        data = service.get_notification_config(user_id)
        configs = data["config"]  

        current = next((config for config in configs if config["id"] == config_id), None)
        if not current:
            return jsonify({"error": "Config not found"}), 404

        new_status = not current["is_enabled"]
        service.update_notification_status(user_id, config_id, new_status)
        return jsonify({"success": True})
    except Exception as e:
        print(f"[ERROR] Toggle failed: {e}")
        return jsonify({"error": str(e)}), 500




from flask import Blueprint, request, jsonify
from services.admin_service import AdminService

admin_routes = Blueprint('admin_routes', __name__)

@admin_routes.route("/admin/servers/status", methods=["GET"])
def get_servers_status():
    data = AdminService().list_external_servers_status()
    return jsonify([
        {
            "ExternalId": row[0],
            "Name": row[1],
            "IsActive": row[2],
            "LastAccessed": str(row[3])
        }
        for row in data
    ])

@admin_routes.route("/admin/servers/details", methods=["GET"])
def get_servers_details():
    data = AdminService().list_external_servers_details()
    return jsonify([
        {
            "ServerId": record[0],
            "Name": record[1],
            "ApiKey": record[2]
        }
        for record in data
    ])

@admin_routes.route("/admin/servers/update", methods=["PATCH"])
def update_server_api_key():
    body = request.get_json()
    AdminService().update_server_api_key(body["server_id"], body["new_key"])
    return jsonify({"success": True})

@admin_routes.route("/admin/categories", methods=["POST"])
def add_category():
    data = request.json
    try:
        name = data["name"]
        admin_id = data["admin_id"]
        AdminService().add_category(name, admin_id)
        return jsonify({"message": "Category added successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


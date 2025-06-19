from flask import Blueprint, request, jsonify
from services.auth_service import AuthService

auth_routes = Blueprint('auth_routes', __name__, url_prefix="/api/auth")
auth_service = AuthService()

@auth_routes.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "User")  
    result = auth_service.register_user(name, email, password, role)
    return jsonify(result)

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    result = auth_service.login_user(email, password)
    return jsonify(result)

@auth_routes.route('/check_email', methods=['POST'])
def check_email():
    data = request.json
    email = data.get("email")
    is_taken = auth_service.is_email_registered(email)
    return jsonify({"exists": is_taken})


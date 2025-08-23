from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from ..models import User
from ..extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('username')
    password = data.get('password')
    if not name or not password:
        return "Username and password are required", 400
    if User.query.filter_by(name=name).first():
        return "Username already exists", 400
    hashed_password = generate_password_hash(password)
    new_user = User(name=name, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return "User registered successfully", 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    name = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(name=name).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=str(user.id))
        return {'access_token': access_token, 'user_id': user.id}, 200
    return {"message": "Invalid username or password"}, 401

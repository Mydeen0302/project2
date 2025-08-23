from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import User

protected_bp = Blueprint('protected', __name__)

@protected_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    user_id_str = get_jwt_identity()
    user_id = int(user_id_str)
    user = User.query.get(user_id)
    if not user:
        return jsonify(message="User not found"), 401
    return jsonify(message=f"Hello, {user.name}! You accessed a protected route.")

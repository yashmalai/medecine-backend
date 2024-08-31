from flask import Blueprint, jsonify, session
from app.models import User

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/user', methods=['GET'])
def get_user():
    users = User.query.all()
    users_list = [{'id': user.id, 'name': user.name, 'age': user.age, 'weight':user.weight, 'height':user.height} for user in users]
    return jsonify(users_list)

@user_bp.route('/user/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logout successful"}), 200
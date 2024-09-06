from flask import Blueprint, jsonify, request
from app.models import User
from app.extensions import db

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/user', methods=['GET'])
def get_user():
    username = request.args.get('name')
    current_user = User.query.filter_by(name=username).first()
    user_data_list = {'id': current_user.id, 'name': current_user.name, 'age': current_user.age, 'weight': current_user.weight, 'height': current_user.height}
    return jsonify(user_data_list)


@user_bp.route('/delete_user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200

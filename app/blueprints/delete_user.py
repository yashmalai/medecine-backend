from flask import Blueprint, jsonify, session
from app.models import User
from app.extensions import db

delete_user_bp = Blueprint('delete_user_bp', __name__)

@delete_user_bp.route('/delete_user/<int:id>', methods=['DELETE'])
def delete_user():
    if 'id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session['id']
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    session.pop('id', None)

    return jsonify({"message": "User deleted successfully"}), 200
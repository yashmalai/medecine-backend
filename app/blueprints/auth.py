from flask import Blueprint, jsonify, session, request
from app.extensions import db
from app.models import User

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    weight = data.get('weight')
    height = data.get('height')
    password = data.get('password')

    if not all([name, age, weight, height, password]):
        return jsonify({"error": "All fields are required"}), 400

    existing_user = User.query.filter_by(name=name).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    new_user = User(
        name=name,
        age=age,
        weight=weight,
        height=height,
        password=password
        )
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')

    user = User.query.filter_by(name=name).first()
    if user and User.check_password(password):
        session['user_id'] = user.id
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid name or password"}), 401
    



    

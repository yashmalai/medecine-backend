from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import training
from datetime import datetime

training_bp = Blueprint('training_bp', __name__)

@training_bp.route('/training', methods=['GET'])
def get_trainings():
    trainings = training.query.all()
    training_list = [{'id': w.id, 'name': w.name, 'workout_type': w.workout_type} for w in trainings]
    return jsonify(training_list)

@training_bp.route('/training/run', methods=['GET'])
def run_training():
    trainings = training.query.filter(training.workout_type == 'run').all()
    training_list = [{'id': w.id, 'name': w.name, 'workout_type': w.workout_type} for w in trainings]
    return jsonify(training_list)

@training_bp.route('/training/run', methods=['POST'])
def add_training():
    data = request.json
    new_training = training(
        name=data.get('name'), 
        workout_type=data.get('workout_type'),
        workout_subtype = data.get('workout_subtype'),
        calories = data.get('calories'),
        spec_conditions = data.get('spec_conditions'),
        date = datetime.strptime(data.get('date'), '%Y-%m-%d').date(),
        time = datetime.strptime(data.get('time'), '%H:%m:%s').time(),
        created_at = datetime.now()
        )
    db.session.add(new_training)
    db.session.commit()
    return jsonify({'message': 'Training added successfully'}), 201

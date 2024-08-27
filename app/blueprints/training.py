from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import training, journal
from datetime import datetime

training_bp = Blueprint('training_bp', __name__)

def journal_entry(action_type, action_id):
    return journal(
        action_type=action_type, 
        action_id=action_id, 
        created_at=datetime.now()
    )

@training_bp.route('/training', methods=['GET'])
def get_trainings():
    trainings = training.query.all()
    training_list = [{'id': w.id, 'name': w.name, 'workout_type': w.workout_type} for w in trainings]
    return jsonify(training_list)

@training_bp.route('/training', methods=['POST'])
def add_training():
    data = request.json
    new_training = training(
        name=data.get('name'), 
        workout_type=data.get('workout_type'),
        workout_subtype = data.get('workout_subtype'),
        calories = data.get('calories'),
        spec_conditions = data.get('spec_conditions'),
        start_date = datetime.strptime(data.get('date'), '%Y-%m-%d').date(),
        duration = datetime.strptime(data.get('time'), '%H:%m:%s').time(),
        created_at = datetime.now()
        )
    db.session.add(new_training)
    db.session.flush()

    new_journal = journal_entry(data.get('drug_type'), new_training.id)
    db.session.add(new_journal)

    db.session.commit()
    return jsonify({'message': 'Training added successfully'}), 201

@training_bp.route('/training/running', methods=['GET'])
def get_run():
    trainings = training.query.filter(training.workout_type == 'run').all()
    training_list = [{'id': w.id, 'name': w.name, 'workout_type': w.workout_type} for w in trainings]
    return jsonify(training_list)

@training_bp.route('/training/swimming', methods=['GET'])
def get_swim():
    trainings = training.query.filter(training.workout_type == 'swimming').all()
    training_list = [{'id': w.id, 'name': w.name, 'workout_type': w.workout_type} for w in trainings]
    return jsonify(training_list)

@training_bp.route('/training/fighting', methods=['GET'])
def get_fight():
    trainings = training.query.filter(training.workout_type == 'fighting').all()
    training_list = [{'id': w.id, 'name': w.name, 'workout_type': w.workout_type} for w in trainings]
    return jsonify(training_list)

from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Workout, Log
from datetime import datetime
from app.handlers import calories_handler

training_bp = Blueprint('training_bp', __name__)


def journal_entry(action_type, action_id):
    return Log(
        action_type=action_type,
        action_id=action_id,
        timestamp=datetime.now()
    )


@training_bp.route('/training', methods=['GET'])
def get_trainings():
    trainings = Workout.query.all()
    trainings_list = [{'id': training.id, 'name': training.name, 'workout_type': training.workout_type,
                       'workout_subtype': training.workout_subtype,
                       'workout_date': training.workout_date,
                       'workout_time': training.workout_time, 'calories': training.calories} for training in trainings]
    return jsonify(trainings_list)


@training_bp.route('/training', methods=['POST'])
def add_medicine():
    data = request.json
    new_training = Workout(
        name=data.get('name'),
        workout_type=data.get('workout_type'),
        workout_subtype=data.get('workout_subtype'),
        workout_date=datetime.strptime(data.get('workout_date'), '%Y-%m-%d').date(),
        workout_time=data.get('workout_time'),
        calories=calories_handler.calc_calories(data.get('workout_type'), data.get('workout_subtype'),
                                                data.get('workout_time')),
        created_at=datetime.now()
    )
    db.session.add(new_training)
    db.session.flush()

    new_journal = journal_entry(data.get('workout_type'), new_training.id)
    db.session.add(new_journal)

    db.session.commit()
    return jsonify({'message': 'Training added successfully'}), 201

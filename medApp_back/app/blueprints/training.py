from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Workout
from datetime import datetime
from app.handlers import calories_handler

training_bp = Blueprint('training_bp', __name__)


@training_bp.route('/training', methods=['GET'])
def get_trainings():
    userid = int(request.args.get('user_id'))
    trainings = Workout.query.filter_by(user_id=userid)
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
        user_id=data.get('user_id'),
        workout_type=data.get('workout_type'),
        workout_subtype=data.get('workout_subtype'),
        workout_date=datetime.strptime(data.get('workout_date'), '%Y-%m-%d').date(),
        workout_time=data.get('workout_time'),
        calories=calories_handler.calc_calories(data.get('workout_type'), data.get('workout_subtype'),
                                                data.get('workout_time'), data.get('weight')),
        created_at=datetime.now()
    )
    db.session.add(new_training)
    db.session.commit()
    return jsonify({'message': 'Training added successfully'}), 201


@training_bp.route('/training/<int:id>', methods=['DELETE'])
def delete_training(id):
    training = Workout.query.get(id)
    db.session.delete(training)
    db.session.commit()
    return jsonify({"message": "Training deleted successfully"}), 204

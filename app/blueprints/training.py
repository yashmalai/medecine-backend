from flask import Blueprint, jsonify
from app.extensions import db
from app.models import training


training_bp = Blueprint('training_bp', __name__)

@training_bp.route('/training', methods=['GET'])
def get_trainings():
    trainings = training.query.all()
    training_list = [{'id': w.id, 'name': w.name, 'duration': w.workout_type} for w in trainings]
    return jsonify(training_list)
from flask import Blueprint, jsonify
from app.extensions import db
from app.models import journal


journal_bp = Blueprint('journal_bp', __name__)

@journal_bp.route('/log', methods=['GET'])
def get_logs():
    logs = journal.query.all()
    logs_list = [{'id': log.id, 'action_type': log.action_type, 'timestamp': log.timestamp, 'action_id': log.action_id} for log in logs]
    return jsonify(logs_list)
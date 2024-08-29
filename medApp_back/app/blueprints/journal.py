from flask import Blueprint, jsonify
from app.extensions import db
from app.models import Log

journal_bp = Blueprint('journal_bp', __name__)


@journal_bp.route('/log', methods=['GET'])
def get_logs():
    logs = Log.query.all()
    logs_list = [{'id': log.id, 'action_type': log.action_type, 'action_id': log.action_id, 'timestamp': log.timestamp} for log in logs]
    return jsonify(logs_list)

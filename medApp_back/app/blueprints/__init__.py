from flask import Blueprint
from . import journal, medicine, training

journal_bp = Blueprint('journal_bp', __name__)
medicine_bp = Blueprint('medicine_bp', __name__)
training_bp = Blueprint('training_bp', __name__)

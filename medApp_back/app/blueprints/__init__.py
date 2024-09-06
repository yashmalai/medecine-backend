from flask import Blueprint
from . import medicine, training, auth, user

medicine_bp = Blueprint('medicine_bp', __name__)
training_bp = Blueprint('training_bp', __name__)
auth_bp = Blueprint('auth_bp', __name__)
user_bp = Blueprint('user_bp', __name__)

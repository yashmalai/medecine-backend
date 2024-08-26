from flask import Blueprint
from . import medicine, training, journal

medicine_bp = Blueprint('medicine_bp', __name__)


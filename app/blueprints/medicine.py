from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import medicine

medicine_bp = Blueprint('medicine_bp', __name__)


@medicine_bp.route('/med', methods=['GET'])
def get_medicines():
    medicines = medicine.query.all()
    medicines_list = [{'id': med.id, 'name': med.name, 'dose': med.dose, 'unit': med.drug_type, 'intake_rule': med.intake_rule, 'comment': med.comment} for med in medicines]
    return jsonify(medicines_list)
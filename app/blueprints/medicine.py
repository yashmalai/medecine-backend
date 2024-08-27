from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import medicine, journal
from datetime import datetime

medicine_bp = Blueprint('medicine_bp', __name__)


def journal_entry(action_type, action_id):
    return journal(
        action_type=action_type, 
        action_id=action_id, 
        created_at=datetime.now()
    )

@medicine_bp.route('/med', methods=['GET'])
def get_medicines():
    medicines = medicine.query.all()
    medicines_list = [{'id': med.id, 'name': med.name, 'dose': med.dose, 'unit': med.drug_type, 'intake_rule': med.intake_rule, 'comment': med.comment} for med in medicines]
    return jsonify(medicines_list)

@medicine_bp.route('/med', methods=['POST'])
def add_medicine():
    data = request.json
    new_medicine = medicine(
        name=data.get('name'),
        dose=data.get('dose'),
        drug_type=data.get('drug_type'),
        intake_rule=data.get('intake_rule'),
        comment=data.get('comment'),
        schedule_times=data.get('schedule_times'),
        days_of_week=data.get('days_of_week'),
        start_date=datetime.strptime(data.get('start_date'), '%Y-%m-%d').date(),
        end_date=datetime.strptime(data.get('end_date'), '%Y-%m-%d').date() if data.get('end_date') else None,
        created_at=datetime.now()
    )
    db.session.add(new_medicine)
    db.session.flush()

    new_journal = journal_entry(data.get('drug_type'), new_medicine.id)
    db.session.add(new_journal)
    
    db.session.commit()


    return jsonify({'message': 'Medicine added successfully'}), 201
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Drug, Log
from datetime import datetime
from app.handlers import d_days_handler

medicine_bp = Blueprint('medicine_bp', __name__)


def journal_entry(action_type, action_id):
    return Log(
        action_type=action_type,
        action_id=action_id,
        timestamp=datetime.now()
    )


@medicine_bp.route('/medicine', methods=['GET'])
def get_medicines():
    medicines = Drug.query.all()
    medicines_list = [{'id': med.id, 'name': med.name, 'dose': med.dose, 'drug_type': med.drug_type,
                       'intake_rule': med.intake_rule, 'comment': med.comment, 'schedule_times': med.schedule_times,
                       'days_of_week': med.days_of_week, 'start_date': med.start_date, 'end_date': med.end_date,
                       'total_doses': med.total_doses, 'doses_taken': med.doses_taken,
                       'created_at': med.created_at} for med in medicines]
    return jsonify(medicines_list)


@medicine_bp.route('/medicine', methods=['POST'])
def add_medicine():
    data = request.json
    doses_list = {'dose': data.get('dose'), 'schedule': data.get('schedule_times'),
                   'start_date': datetime.strptime(data.get('start_date'), '%Y-%m-%d').date(),
                   'end_date': datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()}
    new_medicine = Drug(
        name=data.get('name'),
        dose=data.get('dose'),
        drug_type=data.get('drug_type'),
        intake_rule=data.get('intake_rule'),
        comment=data.get('comment'),
        schedule_times=data.get('schedule_times'),
        days_of_week=data.get('days_of_week'),
        start_date=datetime.strptime(data.get('start_date'), '%Y-%m-%d').date(),
        end_date=datetime.strptime(data.get('end_date'), '%Y-%m-%d').date(),
        total_doses=d_days_handler.calculate_drug_days(**doses_list),
        created_at=datetime.now()
    )
    db.session.add(new_medicine)
    db.session.flush()

    new_journal = journal_entry(data.get('drug_type'), new_medicine.id)
    db.session.add(new_journal)
    db.session.commit()
    return jsonify({'message': 'Medicine added successfully'}), 201

from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Drug
from datetime import datetime
from datetime import date

medicine_bp = Blueprint('medicine_bp', __name__)


@medicine_bp.route('/medicine', methods=['GET'])
def get_medicines():
    userid = int(request.args.get('user_id'))
    medstat = request.args.get('med_status')
    medicines_ongoing = Drug.query.filter_by(user_id=userid, med_status='ongoing')
    for meds in medicines_ongoing:
        if meds.start_date <= date.today():
            meds.med_status = 'active'
    db.session.commit()
    medicines = Drug.query.filter_by(user_id=userid, med_status=medstat)
    medicines_list = [{'id': med.id, 'name': med.name, 'dose': med.dose, 'drug_type': med.drug_type,
                       'intake_rule': med.intake_rule, 'comment': med.comment, 'intake_time': med.intake_time,
                       'schedule_times': med.schedule_times, 'start_date': med.start_date, 'end_date': med.end_date,
                       'total_doses': med.total_doses, 'doses_taken': med.doses_taken,
                       'created_at': med.created_at} for med in medicines]
    return jsonify(medicines_list)


@medicine_bp.route('/medicine', methods=['POST'])
def add_medicine():
    data = request.json
    new_medicine = Drug(
        name=data.get('name'),
        user_id=data.get('user_id'),
        dose=data.get('dose'),
        drug_type=data.get('drug_type'),
        intake_rule=data.get('intake_rule'),
        comment=data.get('comment'),
        intake_time=data.get('intake_time'),
        schedule_times=data.get('schedule_times'),
        start_date=datetime.strptime(data.get('start_date'), '%d/%m/%Y').date(),
        end_date=datetime.strptime(data.get('end_date'), '%d/%m/%Y').date(),
        total_doses=data.get('total_doses'),
        med_status=data.get('med_status'),
        created_at=datetime.now()
    )
    db.session.add(new_medicine)
    db.session.commit()
    return jsonify({'message': 'Medicine added successfully'}), 201


@medicine_bp.route('/medicine/takemeds', methods=['POST'])
def medicine_take_meds():
    med_id = int(request.args.get('id'))
    med_doses_taken = int(request.args.get('doses_taken'))
    med = Drug.query.get(med_id)
    med.doses_taken = med_doses_taken
    if med_doses_taken == med.total_doses:
        med.med_status = 'completed'
    db.session.commit()
    return jsonify({'message': 'Medicine modified successfully'}), 201

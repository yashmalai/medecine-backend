from flask import jsonify
from app import create_app
from app.models import medicine


app = create_app()
'''
@app.route('/medicine', methods=['GET'])
def get_medicines():
    medicines = medicine.query.all()
    medicines_list = [{'id': med.id, 'name': med.name, 'dose': med.dose, 'unit': med.drug_type, 'intake_rule': med.intake_rule, 'comment': med.comment} for med in medicines]
    return jsonify(medicines_list)
'''


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

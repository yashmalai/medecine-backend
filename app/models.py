from app.extensions import db
from datetime import datetime

class menu(db.Model):
    __tablename__ ='menu'
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(255))
    created = db.Column("created", db.DateTime)
    modified = db.Column("modified", db.DateTime)

    def __init__(self, name, email):
        self.name = name

class medicine(db.Model):
    __tablename__ = 'drug'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dose = db.Column(db.String(50), nullable=False)
    drug_type = db.Column(db.String(20), nullable=False)
    intake_rule = db.Column(db.String(50), nullable=False) #правила приема
    comment = db.Column(db.Text, nullable=True)
    schedule_times = db.Column(db.String(256), nullable=False)  # Хранение времени в виде строки, разделенной запятыми "08002000"
    days_of_week = db.Column(db.String(7), nullable=False)  # Хранение дней в виде строки из "1" и "0" для каждого дня недели "1100000"
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, name, dose, drug_type, intake_rule, comment, schedule_times, days_of_week, start_date, end_date, created_at): 
        self.name = name
        self.dose = dose
        self.drug_type = drug_type
        self.intake_rule = intake_rule
        self.comment = comment
        self.schedule_times = schedule_times
        self.days_of_week = days_of_week
        self.start_date = start_date
        self.end_date = end_date
        self.created_at = created_at


class journal(db.Model):
    __tablename__ = 'journal'

    id = db.Column(db.Integer, primary_key=True)
    action_type = db.Column(db.String(50), nullable=False)  # 'medicine' or 'workout'
    timestamp = db.Column(db.DateTime, default=datetime.now())
    action_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, action_type, medicine_id=None, workout_id=None, comment=None):
        self.action_type = action_type
        self.medicine_id = medicine_id
        self.workout_id = workout_id
        self.comment = comment

class training(db.Model):
    __tablename__ = 'workout'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)    
    workout_type = db.Column(db.String(20), nullable=False)
    workout_subtype = db.Column(db.String(20), nullable=True) #уникальные свойства вида спорта
    calories = db.Column(db.Integer, nullable=True)
    spec_conditions = db.Column(db.Integer, nullable=True) #специальное условие
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime)

    def __init__(self, name, workout_type, workout_subtype, calories, spec_conditions, date, time):
        self.name = name
        self.workout_type = workout_type
        self.workout_subtype = workout_subtype
        self.calories = calories
        self.spec_conditions = spec_conditions
        self.date = date
        self.time = time

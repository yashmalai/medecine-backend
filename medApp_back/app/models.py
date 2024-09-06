from app.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    drugs = db.relationship('Drug', backref='users', cascade="all,delete")
    workouts = db.relationship('Workout', backref='users', cascade="all,delete")

    def __init__(self, name, age, weight, height, password, created_at):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height
        self.password_hash = generate_password_hash(password)
        self.created_at = created_at

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Drug(db.Model):
    __tablename__ = 'drugs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    dose = db.Column(db.String(50), nullable=False)
    drug_type = db.Column(db.String(50), nullable=False)
    intake_rule = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.Text, nullable=True)
    intake_time = db.Column(db.String(200), nullable=False)  # Хранение времени в виде строки, разделенной запятыми "08:00,20:00"
    schedule_times = db.Column(db.String(500), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    doses_taken = db.Column(db.Integer, nullable=True, default=0)
    total_doses = db.Column(db.Integer, nullable=True)
    med_status = db.Column(db.String(25), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Workout(db.Model):
    __tablename__ = 'workouts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    workout_type = db.Column(db.String(50), nullable=False)
    workout_subtype = db.Column(db.String(50), nullable=False)
    workout_date = db.Column(db.Date, nullable=False)
    workout_time = db.Column(db.Integer, nullable=False)
    calories = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


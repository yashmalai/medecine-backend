from app.extensions import db
from datetime import datetime


class Drug(db.Model):
    __tablename__ = 'drug'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dose = db.Column(db.String(50), nullable=False)
    drug_type = db.Column(db.String(20), nullable=False)
    intake_rule = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.Text, nullable=True)
    schedule_times = db.Column(db.String(200), nullable=False)  # Хранение времени в виде строки, разделенной запятыми "08:00,20:00"
    days_of_week = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    doses_taken = db.Column(db.Integer, nullable=True, default=0)
    total_doses = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Workout(db.Model):
    __tablename__ = 'workout'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    workout_type = db.Column(db.String(20), nullable=False)
    workout_subtype = db.Column(db.String(20), nullable=False)
    workout_date = db.Column(db.Date, nullable=False)
    workout_time = db.Column(db.Integer, nullable=False)
    calories = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    action_type = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    action_id = db.Column(db.Integer, nullable=True)

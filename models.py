from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(10), nullable=False)  # "host" or "charity"
    donations = db.relationship('FoodDonation', backref='host', lazy=True)

class FoodDonation(db.Model):
    __tablename__ = 'food_donations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    host_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    food_type = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)
    city = db.Column(db.String(80), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(10), default="available")

class DonationRequest(db.Model):
    __tablename__ = 'donation_requests'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    charity_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    donation_id = db.Column(db.Integer, db.ForeignKey('food_donations.id'), nullable=False)
    request_date = db.Column(db.DateTime, default=datetime.utcnow)

    donation = db.relationship('FoodDonation', backref='requests', lazy=True)
    charity = db.relationship('User', foreign_keys=[charity_id])

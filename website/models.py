from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    notes = db.relationship('Note')

class CarbonEmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transportation = db.Column(db.Float, nullable=False)
    energy = db.Column(db.Float, nullable=False)
    diet = db.Column(db.String(20), nullable=False)
    waste = db.Column(db.Float, nullable=False)
    total_emission = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())


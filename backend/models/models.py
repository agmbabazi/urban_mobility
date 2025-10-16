# Database models will be setup here
# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TripModel(db.Model):
    __tablename__ = 'trips'

    trip_id = db.Column(db.Integer, primary_key=True)
    pickup_datetime = db.Column(db.DateTime)
    dropoff_datetime = db.Column(db.DateTime)
    pickup_lat = db.Column(db.Float)
    pickup_lng = db.Column(db.Float)
    dropoff_lat = db.Column(db.Float)
    dropoff_lng = db.Column(db.Float)
    fare_amount = db.Column(db.Float)
    tip_amount = db.Column(db.Float)
    distance_km = db.Column(db.Float)
    duration_min = db.Column(db.Float)
    passenger_count = db.Column(db.Integer)

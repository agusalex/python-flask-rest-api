import json

from app import db


class Factory(db.Model):
    __tablename__ = 'factories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chart_data = db.Column(db.JSON, nullable=False)

    def __init__(self, factory_data):
        chart_data = factory_data['chart_data']
        self.chart_data = json.dumps({
            'sprocket_production_actual': chart_data['sprocket_production_actual'],
            'sprocket_production_goal': chart_data['sprocket_production_goal'],
            'time': chart_data['time']
        })

    def serialize(self):
        return {"factory": {"chart_data": json.loads(self.chart_data)}}


class Sprocket(db.Model):
    __tablename__ = 'sprockets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teeth = db.Column(db.Integer, nullable=False)
    pitch_diameter = db.Column(db.Float, nullable=False)
    outside_diameter = db.Column(db.Float, nullable=False)
    pitch = db.Column(db.Float, nullable=False)

    def __init__(self, teeth, pitch_diameter, outside_diameter, pitch):
        self.teeth = teeth
        self.pitch_diameter = pitch_diameter
        self.outside_diameter = outside_diameter
        self.pitch = pitch

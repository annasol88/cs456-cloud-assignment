
from flask_sqlalchemy import SQLAlchemy

"""
An ORM package to map the python objects to DB tables using flask-sqlalchemy.
All classes contain the respective attributes that align with a DB schema,
an __init__ function to initialise an Object of its type
as well as a to_dict representation to convert a given object into JSON format returned in webapp requests.
"""


db = SQLAlchemy()


"""
Representing a Turbine object inside the turbine_monitor DB
"""
class Turbine(db.Model):
    __tablename__ = 'turbine'
    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.CHAR(25), nullable=False)
    
    measurements = db.relationship('Measurement', backref='measurements', lazy=True)

    def __init__(
            self,
            serial: str = "",) -> None:
        self.serial = serial

    def to_dict(self) -> dict:
        return { "serial": self.serial, }


"""
Representing a Measurement object inside the turbine_monitor DB
"""
class Measurement(db.Model):
    __tablename__ = 'measurement'
    id = db.Column(db.Integer, primary_key=True)
    turbine_id = db.Column(db.Integer, db.ForeignKey('turbine.id'), nullable=False)
    wind_speed_mean = db.Column(db.Float, nullable=False)
    wind_speed_stdev = db.Column(db.Float, nullable=False)
    pitch_mean = db.Column(db.Float, nullable=True)
    pitch_stdev = db.Column(db.Float, nullable=True)
    power_mean = db.Column(db.Float, nullable=True)
    power_stdev = db.Column(db.Float, nullable=True)
    n_samples = db.Column(db.Integer, nullable=False)
    samples_from = db.Column(db.DATETIME, nullable=False)
    samples_to = db.Column(db.DATETIME, nullable=False)

    def __init__(
            self, 
            turbine_id,
            wind_speed_mean, 
            wind_speed_stdev,
            pitch_mean, 
            pitch_stdev, 
            power_mean,
            power_stdev,
            n_samples,
            samples_from,
            samples_to) -> None:
        self.turbine_id = turbine_id
        self.wind_speed_mean = wind_speed_mean
        self.wind_speed_stdev = wind_speed_stdev
        self.pitch_mean = pitch_mean
        self.pitch_stdev = pitch_stdev
        self.power_mean = power_mean
        self.power_stdev = power_stdev
        self.n_samples = n_samples
        self.samples_from = samples_from
        self.samples_to = samples_to
        

    def to_dict(self) -> dict:
        return {
            "wind_speed_mean": self.wind_speed_mean,
            "wind_speed_stdev": self.wind_speed_stdev,
            "pitch_mean": self.pitch_mean,
            "pitch_stdev": self.pitch_stdev,
            "power_mean": self.power_mean,
            "power_stdev":self.power_stdev,
            "n_samples": self.n_samples,
            "samples_from": self.samples_from.isoformat(),
            "samples_to": self.samples_to.isoformat()
        }

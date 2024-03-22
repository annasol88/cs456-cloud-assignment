
from sqlalchemy import CHAR, DATETIME, Column, Float, ForeignKey, Integer
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime


Base = declarative_base()


class Turbine(Base):
    __tablename__ = 'turbine'
    id = Column(Integer, primary_key=True)
    serial = Column(CHAR(25), nullable=False)
    
    measurements = relationship('Measurement', backref='measurements', lazy=True)

    def __init__(self,
                 serial: str = "",
                ) -> None:
        self.serial = serial

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "serial": self.serial,
        }

    def from_dict(self, data_dict: dict) -> None:
        for key in data_dict:
            if key == "id":
                continue
            setattr(self, key, data_dict[key])


class Measurement(Base):
    __tablename__ = 'measurement'
    id = Column(Integer, primary_key=True)
    turbine_id = Column(Integer, ForeignKey('turbine.id'), nullable=False)
    wind_speed_mean = Column(Float, nullable=False)
    wind_speed_stdev = Column(Float, nullable=False)
    pitch_mean = Column(Float, nullable=True)
    pitch_stdev = Column(Float, nullable=True)
    power_mean = Column(Float, nullable=True)
    power_stdev = Column(Float, nullable=True)
    n_samples = Column(Integer, nullable=False)
    samples_from = Column(DATETIME, nullable=False)
    samples_to = Column(DATETIME, nullable=False)

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
            "id": self.id,
            "turbine_id": self.turbine_id,
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


class Measurement_Record():
    def __init__(self, wind_speed, pitch, power, timestamp):
        self.wind_speed: int = wind_speed
        self.pitch: int = pitch
        self.power: int = power
        self.timestamp: datetime = datetime.fromisoformat(timestamp)
        
    def __str__(self):
        return f"measurment: {self.wind_speed}, {self.pitch}, {self.power}, {self.timestamp}"
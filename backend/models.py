from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from .database import Base

class WeatherRecord(Base):
    __tablename__ = "weather_records"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Raw values from WSLink
    temp_out = Column(Float) # t1tem
    humidity_out = Column(Integer) # t1hum
    wind_dir = Column(Integer) # t1wdir
    wind_speed = Column(Float) # t1ws
    rain_daily = Column(Float) # t1raindy
    solar_radiation = Column(Float) # t1solrad
    uv_index = Column(Float) # t1uvi
    
    # Indoor values (optional but good to have)
    temp_in = Column(Float, nullable=True) # intem
    humidity_in = Column(Integer, nullable=True) # inhum
    pressure_rel = Column(Float, nullable=True) # rbar
    
    def __repr__(self):
        return f"<WeatherRecord(time={self.timestamp}, temp={self.temp_out})>"

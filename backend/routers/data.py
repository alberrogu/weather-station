from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from ..database import get_db
from ..models import WeatherRecord
from pydantic import BaseModel

router = APIRouter(prefix="/api")

# Pydantic models for response
class WeatherData(BaseModel):
    id: int
    timestamp: datetime
    temp_out: Optional[float]
    humidity_out: Optional[int]
    wind_dir: Optional[int]
    wind_speed: Optional[float]
    rain_daily: Optional[float]
    solar_radiation: Optional[float]
    uv_index: Optional[float]
    pressure_rel: Optional[float]

    class Config:
        orm_mode = True

@router.get("/current", response_model=Optional[WeatherData])
def get_current_weather(db: Session = Depends(get_db)):
    """Get the most recent weather record."""
    latest = db.query(WeatherRecord).order_by(WeatherRecord.timestamp.desc()).first()
    if not latest:
        return None
    return latest

@router.get("/history", response_model=List[WeatherData])
def get_history(hours: int = 24, db: Session = Depends(get_db)):
    """Get historical data for charts."""
    since = datetime.utcnow() - timedelta(hours=hours)
    records = db.query(WeatherRecord).filter(WeatherRecord.timestamp >= since).order_by(WeatherRecord.timestamp.asc()).all()
    return records

class DailyRainData(BaseModel):
    timestamp: datetime
    rain_daily: float

@router.get("/history/rain", response_model=List[DailyRainData])
def get_rain_history(days: int = 7, db: Session = Depends(get_db)):
    """Get max daily rain for the last X days."""
    since = datetime.utcnow() - timedelta(days=days)
    records = db.query(WeatherRecord).filter(WeatherRecord.timestamp >= since).all()
    
    daily_max = {}
    for r in records:
        if r.rain_daily is None:
            continue
        date_key = r.timestamp.date().isoformat()
        if date_key not in daily_max or r.rain_daily > daily_max[date_key]:
            daily_max[date_key] = r.rain_daily
            
    result = []
    for i in range(days - 1, -1, -1):
        d = (datetime.utcnow() - timedelta(days=i)).date()
        date_key = d.isoformat()
        dt = datetime.combine(d, datetime.min.time())
        result.append({
            "timestamp": dt,
            "rain_daily": daily_max.get(date_key, 0.0)
        })
    return result

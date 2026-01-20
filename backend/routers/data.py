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

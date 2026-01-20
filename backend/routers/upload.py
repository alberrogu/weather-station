from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import get_db
from ..models import WeatherRecord
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/data/upload.php")
async def upload_data(
    request: Request,
    db: Session = Depends(get_db),
    wsid: str = Query(None),
    wspw: str = Query(None),
    # Datetime might be passed or we use current time
    dt: str = Query(None, alias="datetime"),
    # Sensors
    temp_out: float = Query(None, alias="t1tem"),
    humidity_out: int = Query(None, alias="t1hum"),
    wind_dir: int = Query(None, alias="t1wdir"),
    wind_speed: float = Query(None, alias="t1ws"),
    rain_daily: float = Query(None, alias="t1raindy"),
    solar_radiation: float = Query(None, alias="t1solrad"),
    uv_index: float = Query(None, alias="t1uvi"),
    # Indoor/Other
    temp_in: float = Query(None, alias="intem"),
    humidity_in: int = Query(None, alias="inhum"),
    pressure_rel: float = Query(None, alias="rbar"),
):
    """
    Endpoint for WSLink weather station data upload.
    Format: GET /data/upload.php?wsid=...
    """
    # Log incoming request details
    logger.info(f"Received Upload Request from {request.client.host}")
    logger.info(f"Params: wsid={wsid}, wspw={wspw}, dt={dt}, temp={temp_out}, hum={humidity_out}, wind={wind_speed}@{wind_dir}")
    logger.debug(f"Full Query Params: {request.query_params}")

    # Basic Authorization Check (can be expanded)
    # if wsid != EXPECTED_ID or wspw != EXPECTED_PW:
    #     raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        current_time = datetime.utcnow()
        if dt:
            try:
                # Attempt to parse datetime if provided
                # Format example: 2000-01-01 10:32:25
                current_time = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                pass # Use server time if parse fails
        
        record = WeatherRecord(
            timestamp=current_time,
            temp_out=temp_out,
            humidity_out=humidity_out,
            wind_dir=wind_dir,
            wind_speed=wind_speed,
            rain_daily=rain_daily,
            solar_radiation=solar_radiation,
            uv_index=uv_index,
            temp_in=temp_in,
            humidity_in=humidity_in,
            pressure_rel=pressure_rel
        )
        
        db.add(record)
        db.commit()
        db.refresh(record)
        
        return {"status": "success", "id": record.id}
        
    except Exception as e:
        logger.error(f"Error saving weather data: {e}")
        # WSLink expects 200 OK usually, but we can return 500 if critical
        raise HTTPException(status_code=500, detail=str(e))

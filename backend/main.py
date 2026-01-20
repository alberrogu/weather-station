from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("weather_station")

from .database import engine, Base
from .routers import upload, data

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Weather Station Server")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"----------------------------------------------------------------")
    logger.info(f"Incoming Request: {request.method} {request.url}")
    
    # Log Headers
    headers = dict(request.headers)
    logger.info(f"Headers: {headers}")

    # Log Body
    try:
        body_bytes = await request.body()
        body_str = body_bytes.decode("utf-8", errors="replace")
        if body_str:
            logger.info(f"Body: {body_str}")
        else:
            logger.info("Body: <empty>")
    except Exception as e:
        logger.error(f"Error reading body: {e}")

    try:
        response = await call_next(request)
        logger.info(f"Response Status: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Request Failed: {e}")
        raise

# Include Routers
app.include_router(upload.router)
app.include_router(data.router)

# Mount static files for frontend (we will build React to 'static' folder later)
# Mount static files for frontend
path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(path):
    app.mount("/", StaticFiles(directory=path, html=True), name="static")

@app.get("/")
def read_root():
    return {"message": "Weather Station API is running. Go to /docs for API documentation."}

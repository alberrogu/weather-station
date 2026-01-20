# Weather Station Server

A self-hosted Weather Station server compatible with **WSLink** devices. It collects data from your weather station, stores it locally, and visualizes it on a modern, responsive dashboard.

## Features

-   **WSLink Compatible**: Works with standard weather station upload protocol.
-   **Dashboard**: Premium React-based UI with Light/Dark mode.
-   **Metrics**: Temperature, Humidity, Wind Speed/Direction, Precipitation, UV Index, Light Intensity, and Pressure (Barometer).
-   **History**: 24-hour historical charts.
-   **Home Assistant**: Ready to be installed as an HA Add-on.
-   **Docker**: Fully containerized.

## Quick Start (Docker)

Run the container on port 80:

```bash
docker run -d \
  --name weather-station \
  -p 80:80 \
  -v weather_data:/app/weather.db \
  albertferlo/weather-station:latest
```

### Data Persistence
To ensure your weather history (database) survives container restarts or updates, you **must** mount a volume for the database file.

The database is located at `/app/weather.db` inside the container.

**Using a named volume:**
```bash
-v weather_data:/app/weather.db
```
(Note: You might need to map the file specifically if using bind mounts, or map the parent directory if preferred, but the app expects the DB at root `/app/weather.db`).

**Using a bind mount (Host folder):**
```bash
-v /path/to/your/data/weather.db:/app/weather.db
```

## Configuration

Configure your Weather Station device (e.g., via mobile app) with:

-   **Server IP**: Your server/computer IP.
-   **Port**: `80`
-   **Path**: `/data/upload.php`
-   **WSID/Password**: Any string (server accepts all by default).

## Development

1.  **Backend**: FastAPI (Python)
2.  **Frontend**: React + Vite
3.  **Database**: SQLite (SQLAlchemy)

### Run Locally
```bash
# Backend
pip install -r requirements.txt
uvicorn backend.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

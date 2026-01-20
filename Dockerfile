# Build Frontend
FROM node:18-alpine as frontend-build
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Python Backend
FROM python:3.11-slim
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Backend Code
COPY backend/ ./backend/

# Copy Frontend Build to static folder
# We place it inside backend/static so FastAPI can serve it
COPY --from=frontend-build /app/frontend/dist ./backend/static

# Expose port
EXPOSE 80

# Run script
COPY run.sh .
RUN chmod +x run.sh

CMD ["./run.sh"]

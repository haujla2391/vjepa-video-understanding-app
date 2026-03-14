FROM python:3.11

WORKDIR /app

# Fix: Use root requirements.txt (not backend/)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code (frontend folder will be at /app/frontend)
COPY . .

# No npm, no build — just copy the files as-is

CMD ["sh", "-c", "uvicorn backend.app:app --host 0.0.0.0 --port ${PORT:-7860}"]
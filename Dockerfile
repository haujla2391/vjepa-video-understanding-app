FROM python:3.11

WORKDIR /app

# Install deps first for better caching
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else
COPY . .

# Use port 7860 — HF Spaces expects this by default
# Bind to 0.0.0.0 (required — do NOT use 127.0.0.1 or localhost)
# Use $PORT if set, but fallback to 7860
CMD ["sh", "-c", "uvicorn backend.app:app --host 0.0.0.0 --port ${PORT:-7860}"]
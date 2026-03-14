FROM python:3.11

# Install Node.js for building React (use node base or install npm)
RUN apt-get update && apt-get install -y nodejs npm

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything
COPY . .

# Build React frontend (assumes your frontend has package.json with "build" script)
RUN cd frontend && npm install && npm run build

# Optional: If no package.json yet, create minimal one or just copy static files
# For your current plain HTML/JS → no build needed, just copy as-is

CMD ["sh", "-c", "uvicorn backend.app:app --host 0.0.0.0 --port ${PORT:-7860}"]
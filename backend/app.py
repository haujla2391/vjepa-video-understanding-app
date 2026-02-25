import backend.vjepa_path_fix

import os
import shutil
import json
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.model_loader import VJEPAService
from backend.inference import predict

app = FastAPI(title="V-JEPA 2 Video Understanding API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Debug
print("Current working dir:", os.getcwd())
print("Files in frontend folder:", os.listdir("frontend") if os.path.exists("frontend") else "missing")
print("index.html exists?", os.path.exists("frontend/index.html"))

try:
    with open("ssv2_classes.json", "r") as f:
        class_map = json.load(f)
except FileNotFoundError:
    print("Warning: ssv2_classes.json not found")
    class_map = {}

service = VJEPAService()

# Serve static assets (script.js, future css/images) under /static/
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Explicitly serve index.html at root (GET /)
@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

# Your API endpoint – now safe from static mount interference
@app.post("/predict")
async def classify_video(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        top5_indices, top5_probs = predict(service, temp_path)

        results = [
            {"label": class_map.get(str(idx), "Unknown"), "probability": float(prob)}
            for idx, prob in zip(top5_indices, top5_probs)
        ]

        return {"predictions": results}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
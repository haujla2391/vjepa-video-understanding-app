import os
import shutil
import json
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from backend.model_loader import VJEPAService
from backend.inference import predict

# create an instance of FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("ssv2_classes.json", "r") as f:
    class_map = json.load(f)

# Load model once at startup
service = VJEPAService()

# When requests to root URL
@app.get("/")
def read_root():
    return {"message": "VJEPA2 Video Understanding API is running"}

# API endpoint for POST requests at predict
@app.post("/predict")
async def classify_video(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        top5_indices, top5_probs = predict(service, temp_path)

        results = []
        for idx, prob in zip(top5_indices, top5_probs):
            results.append({
                "label": class_map.get(str(idx), "Unknown"),
                "probability": float(prob)
            })

        return {"predictions": results}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
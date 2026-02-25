import os
import shutil
from fastapi import FastAPI, UploadFile, File

from backend.model_loader import VJEPAService
from backend.inference import predict

# create an instance of FastAPI
app = FastAPI()

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

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    top5_indices, top5_probs = predict(service, temp_path)
    os.remove(temp_path)

    return {
        "top5_indices": top5_indices[0],
        "top5_scores": top5_probs[0],
    }
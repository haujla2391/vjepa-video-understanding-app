# vjepa-video-understanding-app
A full-stack video understanding web application built using VJEPA2, a self-supervised video world model developed by Meta AI. The system extracts latent video representations and performs downstream action classification through a trained neural head.

## Dependencies

pip install -r backend/requirements.txt

This project uses Meta AI's VJEPA2 model:

git clone https://github.com/facebookresearch/vjepa2.git

Download the model weights

mkdir models 

(giant models)

wget https://dl.fbaipublicfiles.com/vjepa2/vitg-384.pt -P models 

wget https://dl.fbaipublicfiles.com/vjepa2/evals/ssv2-vitg-384-64x2x3.pt -P models 

(large models)

wget https://dl.fbaipublicfiles.com/vjepa2/vitl.pt -O models/vitl-256.pt

wget https://dl.fbaipublicfiles.com/vjepa2/evals/ssv2-vitl-16x2x3.pt -O models/ssv2-vitl-256-16x2x3.pt

## Installation

### 1. Clone this repo:
git clone https://github.com/haujla2391/vjepa-video-understanding-app.git
cd vjepa-video-understanding-app
### 2. Create Virtual Environment
conda create -n vjepa python=3.11
conda activate vjepa
### 3. Install dependencies
pip install -r requirements.txt
### 4. Clone VJEPA2
git clone https://github.com/facebookresearch/vjepa2.git
### 5. Run backend
uvicorn backend.main:app --reload
### 6. Open frontend in your browser
cd frontend
npm install
npm start

## Architecture

![architecture model](images/mermaid-diagram-2026-02-25-012213.png)

## Techstack

* PyTorch
* FastAPI
* React / HTML
* Self-Supervised Learning
* Video Representation Learning

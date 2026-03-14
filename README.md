---
title: V-JEPA Video Understanding App
emoji: 🎥
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

<div align="center">

<h1>V-JEPA 2 Video Understanding App</h1>

**Real-time next-action prediction from video clips using Meta's V-JEPA 2 foundation model**

<br>

<a href="https://huggingface.co/spaces/haujla2391/VJEPA2">
  <img src="https://img.shields.io/badge/🚀 Live Demo-Hugging Face-blue?style=for-the-badge&logo=huggingface&logoColor=white" alt="Live Demo">
</a>
&nbsp;&nbsp;
<a href="https://github.com/haujla2391/vjepa-video-understanding-app">
  <img src="https://img.shields.io/github/stars/haujla2391/vjepa-video-understanding-app?style=for-the-badge&color=yellow" alt="GitHub Stars">
</a>

<br><br>

![architecture model](images/mermaid-diagram-2026-02-25-012213.png)

</div>

## What it does

This web app lets you upload a short video clip and get **top-5 predicted next actions** using Meta's state-of-the-art **V-JEPA 2** video foundation model (ViT-L backbone + attentive classifier head fine-tuned on Something-Something V2).

Powered by:
- V-JEPA 2 backbone loaded via `torch.hub`
- Attentive classifier probe trained on SSv2 (174 classes)
- FastAPI backend for inference
- Simple, responsive HTML + JavaScript frontend

## Live Demo

Try it now (no installation needed):  
👉 https://haujla2391-vjepa2.hf.space

**Best with short clips (5–15 seconds) of everyday actions** (e.g., someone putting something down, tearing paper, throwing something, etc.).

## Tech Stack

- **Model**: Meta V-JEPA 2 (ViT-Large) + SSv2 attentive probe  
- **Backend**: FastAPI (Python), PyTorch, torch.hub  
- **Frontend**: Vanilla HTML + JavaScript (no heavy framework)  
- **Deployment**: Hugging Face Spaces (Docker)  
- **Video processing**: OpenCV (headless)  
- **Dataset classes**: Something-Something V2 (174 action labels)

Acknowledgments

Meta AI – V-JEPA 2
Something-Something V2 dataset
Inspired by early V-JEPA demos and attentive pooling papers

License
MIT License – feel free to use, modify, and share!
  Built by Harman

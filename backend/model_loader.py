from src.models.attentive_pooler import AttentiveClassifier

import torch
from backend.vjepa_demo import load_pretrained_vjepa_classifier_weights, build_pt_video_transform, device

print("Loading PyTorch V-JEPA 2 backbone via torch.hub...")
hub_output = torch.hub.load('facebookresearch/vjepa2', 'vjepa2_vit_large', pretrained=True)

if isinstance(hub_output, tuple):
    model_pt = hub_output[0]
    print("Hub returned tuple → using first element as backbone")
else:
    model_pt = hub_output

model_pt = model_pt.to(device).eval()

print("Loading Classifier...")
classifier = AttentiveClassifier(
    embed_dim=model_pt.embed_dim,
    num_heads=16,
    depth=4,
    num_classes=174
).to(device).eval()

load_pretrained_vjepa_classifier_weights(
    classifier,
    "models/ssv2-vitl-256-16x2x3.pt"
)

print("Building preprocessing transform...")
pt_video_transform = build_pt_video_transform(img_size=256)

class VJEPAService:
    def __init__(self):
        self.device = device
        self.model_pt = model_pt
        self.classifier = classifier
        self.pt_video_transform = pt_video_transform
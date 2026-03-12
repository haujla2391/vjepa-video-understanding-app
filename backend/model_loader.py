import torch
import sys
import os

# Add the vjepa2 root directory so 'src' is found
vjepa2_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'vjepa2'))
if vjepa2_root not in sys.path:
    sys.path.insert(0, vjepa2_root)

# Now these work
from src.models.attentive_pooler import AttentiveClassifier
from src.models.vision_transformer import vit_large_rope
from backend.vjepa_demo import load_pretrained_vjepa_pt_weights, load_pretrained_vjepa_classifier_weights, build_pt_video_transform, device

device = "cuda" if torch.cuda.is_available() else "cpu"

class VJEPAService:
    # From the demo code provided by Meta

    def __init__(self, pt_model_path, classifier_model_path, img_size=256, num_frames=64):
        self.device = device

        print("Loading PyTorch VJEPA model...")
        self.model_pt = vit_large_rope(img_size=(img_size, img_size), num_frames=num_frames)
        self.model_pt.to(device).eval()
        load_pretrained_vjepa_pt_weights(self.model_pt, pt_model_path)

        print("Loading Classifier...")
        self.classifier = AttentiveClassifier(
            embed_dim=self.model_pt.embed_dim, num_heads=16, depth=4, num_classes=174
        ).to(self.device).eval()
        load_pretrained_vjepa_classifier_weights(self.classifier, classifier_model_path)

        print("Building preprocessing transform...")
        self.pt_video_transform = build_pt_video_transform(img_size=img_size)


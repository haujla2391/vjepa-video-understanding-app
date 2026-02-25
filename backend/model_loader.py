import torch
from transformers import AutoModel, AutoVideoProcessor
from vjepa2.src.models.attentive_pooler import AttentiveClassifier
from vjepa2.src.models.vision_transformer import vit_giant_xformers_rope

device = "cuda" if torch.cuda.is_available() else "cpu"

class VJEPAService:
    # From the demo code provided by Meta

    def __init__(self):
        self.hf_model_name = (
            "facebook/vjepa2-vitg-fpc64-384"  # Replace with your favored model, e.g. facebook/vjepa2-vitg-fpc64-384
        )
        print("Loading HuggingFace model...")

        self.model_hf = AutoModel.from_pretrained(self.hf_model_name).to(device).eval()
        self.hf_transform = AutoVideoProcessor.from_pretrained(self.hf_model_name)
        print("Loading PyTorch backbone...")

        img_size = self.hf_transform.crop_size["height"]  # E.g. 384, 256, etc.
        self.model_pt = vit_giant_xformers_rope(img_size=(img_size, img_size), num_frames=16).to(device).eval()
        print("Loading classifier...")

        self.classifier = (
            AttentiveClassifier(embed_dim=self.model_pt.embed_dim, num_heads=16, depth=4, num_classes=174).to(device).eval()
        )

        print("Model loading complete.")
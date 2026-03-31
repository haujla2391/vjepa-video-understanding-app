from backend.attentive_pooler import AttentiveClassifier

import torch
import os
import urllib.request
from backend.vjepa_demo import load_pretrained_vjepa_classifier_weights, build_pt_video_transform, device

torch.hub._validate_not_a_forked_repo = lambda *args, **kwargs: None

# Fix the broken localhost URL inside vjepa2
def fixed_load_state_dict_from_url(url, *args, **kwargs):
    if "localhost:8300" in url:
        url = "https://dl.fbaipublicfiles.com/vjepa2/vitl.pt"   # correct public URL
        print(f"Fixed localhost URL → {url}")
    return torch.hub._original_load_state_dict_from_url(url, *args, **kwargs)  # need to save original first

# Apply the patch
if not hasattr(torch.hub, '_original_load_state_dict_from_url'):
    torch.hub._original_load_state_dict_from_url = torch.hub.load_state_dict_from_url
torch.hub.load_state_dict_from_url = fixed_load_state_dict_from_url

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

# Official Meta URL for SSV2 ViT-L/16 attentive probe (73.7% top-1)
CLASSIFIER_URL = "https://dl.fbaipublicfiles.com/vjepa2/evals/ssv2-vitl-16x2x3.pt"
LOCAL_DIR = "models"
LOCAL_FILENAME = "ssv2-vitl-16x2x3.pt"  # exact official name
local_path = os.path.join(LOCAL_DIR, LOCAL_FILENAME)

print(f"Creating directory if needed: {LOCAL_DIR}")
os.makedirs(LOCAL_DIR, exist_ok=True)

# Debug: List contents to see what's there
print(f"Current contents of {LOCAL_DIR}: {os.listdir(LOCAL_DIR) if os.path.exists(LOCAL_DIR) else 'Directory does not exist yet'}")

# Force download for reliability (comment out 'True' to use if-not-exists after testing)
FORCE_DOWNLOAD = True  # Set to False once confirmed working

if FORCE_DOWNLOAD or not os.path.exists(local_path):
    print(f"Downloading classifier weights from {CLASSIFIER_URL} to {local_path}...")
    try:
        urllib.request.urlretrieve(CLASSIFIER_URL, local_path)
        print(f"Download successful! File size: {os.path.getsize(local_path) / (1024**2):.2f} MB")
    except Exception as e:
        raise RuntimeError(f"Failed to download classifier: {e}. Check URL/network.")
else:
    print(f"Skipping download — file already at {local_path}")

print(f"Loading weights from {local_path}...")
load_pretrained_vjepa_classifier_weights(classifier, local_path)

print("Building preprocessing transform...")
pt_video_transform = build_pt_video_transform(img_size=256)

class VJEPAService:
    def __init__(self):
        self.device = device
        self.model_pt = model_pt
        self.classifier = classifier
        self.pt_video_transform = pt_video_transform
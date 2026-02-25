import torch
import numpy as np
from decord import VideoReader

device = "cuda" if torch.cuda.is_available() else "cpu"

# from demo code
def get_video(video_path, num_frames=64):
    vr = VideoReader(video_path)
    # sampling 16 frames (or specified amount) from video
    frame_idx = np.linspace(0, len(vr) - 1, num_frames).astype(int)
    video = vr.get_batch(frame_idx).asnumpy()
    return video

def predict(service, video_path):
    video = get_video(video_path, num_frames=64)
    video = torch.from_numpy(video).permute(0, 3, 1, 2) # reorders tensor to # frames, color channels, height, width

    with torch.inference_mode():
        # calls a preprocessing function and returns pytorch tensor
        x_pt = service.pt_video_transform(video).to(device).unsqueeze(0)
        # Extract the patch-wise features from the last layer
        out_patch_features_pt = service.model_pt(x_pt)

        out_classifier = service.classifier(out_patch_features_pt)

        # Apply softmax to full distribution
        probs = torch.softmax(out_classifier, dim=-1)
        top5_probs, top5_indices = torch.topk(probs, 5)
        top5_probs = top5_probs[0] * 100.0
        top5_indices = top5_indices[0]
    
    return top5_indices.cpu().tolist(), top5_probs.cpu().tolist()
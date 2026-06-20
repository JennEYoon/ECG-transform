# 1dcnn inference simple, version 2. Match meta column names.  

# Friday, June 19, 2026 at 8:07:27 PM EDT
# Here is the updated simple code using your exact metadata column names. user_idx # represents the patient, sample_idx represents the 10-second segment, and window_idx # represents the individual heartbeat.


import torch
import pandas as pd
from 1dcnn_copy import ECGNet

# Load data and model
X = pd.read_csv("AR2026.03.csv", header=None).values
meta = pd.read_csv("cnn_ready_metadata_v4.csv")

model = ECGNet(num_classes=6) # class number to check.  
model.load_state_dict(torch.load("saved_model.pth"))
model.eval()

# Run Inference
X_tensor = torch.tensor(X, dtype=torch.float32).unsqueeze(1)
with torch.no_grad():
    outputs = model(X_tensor)
    _, preds = torch.max(outputs, 1)

meta['prediction'] = preds.numpy()

# Aggregate outputs via majority vote (mode)
# 1. Beat level: Grouping the 4 leads per window
beat_diag = meta.groupby(['user_idx', 'sample_idx', 'window_idx'])['prediction'].agg(lambda x: x.mode()[0]).reset_index()

# 2. Segment level: Grouping beats per 10-second sample
segment_diag = beat_diag.groupby(['user_idx', 'sample_idx'])['prediction'].agg(lambda x: x.mode()[0]).reset_index()

# 3. Patient level: Grouping segments per patient
patient_diag = segment_diag.groupby('user_idx')['prediction'].agg(lambda x: x.mode()[0]).reset_index()

print("Patient-level Diagnostics:\n", patient_diag)
print("Segment-level Diagnostics:\n", segment_diag)
print("Beat-level Diagnostics:\n", beat_diag)

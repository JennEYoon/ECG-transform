# 1dcnn inference, simple

import torch
import pandas as pd
from 1dcnn_copy import ECGNet # Import your exact model class

# 1. Load data and model
X = pd.read_csv("AR2026.03.csv", header=None).values
meta = pd.read_csv("cnn_ready_metadata_v4.csv")

model = ECGNet(num_classes=6)
model.load_state_dict(torch.load("saved_model.pth"))
model.eval()

# 2. Run Inference on all 1215 rows
X_tensor = torch.tensor(X, dtype=torch.float32).unsqueeze(1)
with torch.no_grad():
    outputs = model(X_tensor)
    _, preds = torch.max(outputs, 1)

meta['prediction'] = preds.numpy()

# 3. Aggregate outputs via majority vote (mode)
# Beat level (aggregating the 4 leads)
beat_diag = meta.groupby(['patient_id', 'segment_id', 'beat_id'])['prediction'].agg(lambda x: x.mode()[0]).reset_index()

# 10-second segment level
segment_diag = beat_diag.groupby(['patient_id', 'segment_id'])['prediction'].agg(lambda x: x.mode()[0]).reset_index()

# Patient level (60 seconds)
patient_diag = segment_diag.groupby('patient_id')['prediction'].agg(lambda x: x.mode()[0]).reset_index()

print("Patient-level Diagnostics:\n", patient_diag)
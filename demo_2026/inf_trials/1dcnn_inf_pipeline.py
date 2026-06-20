# 1dcnn inference pipeline. meta data file header names adjusted.  

# 1. Standard Python library imports
import datetime
import os
from pathlib import Path

# 2. Third-party imports
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

# 3. Local custom imports (if you had them)
from 1dcnn_copy import ECGNet


def evaluate_ecg_patients(data_path, meta_path, model_path, batch_size=4):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Running inference on: {device}")

    # Load Data
    # AR2026.03.csv has no headers natively
    X_df = pd.read_csv(data_path, header=None)
    meta_df = pd.read_csv(meta_path)
    
    # Initialize Model
    model = ECGNet(num_classes=6).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()

    # Setup DataLoader 
    # Batch size is set to 4 to group the 4 leads (I, II, V2, V5) per beat together
    X_tensor = torch.tensor(X_df.values, dtype=torch.float32).unsqueeze(1)
    dataset = TensorDataset(X_tensor)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

    beat_predictions = []
    
    # Inference
    with torch.no_grad():
        for batch in loader:
            inputs = batch[0].to(device)
            outputs = model(inputs) # Shape: [4, 6] (4 leads, 6 classes)
            
            # Average the logits across the 4 leads to get one consensus prediction for the beat
            avg_logits = outputs.mean(dim=0, keepdim=True) 
            _, pred = torch.max(avg_logits, 1)
            
            # Record the consensus prediction
            beat_predictions.append(pred.item())

    # Map the beat predictions back to the metadata
    # We drop the duplicate lead rows using the exact metadata headers
    meta_beats_only = meta_df.drop_duplicates(subset=['user_idx', 'sample_idx', 'window_idx']).copy()
    
    if len(beat_predictions) != len(meta_beats_only):
        print(f"Warning: Batch output length ({len(beat_predictions)}) does not match unique beats in metadata ({len(meta_beats_only)}).")
        
    meta_beats_only['beat_prediction'] = beat_predictions[:len(meta_beats_only)]

    # Aggregate by 10-second segment
    segment_summary = meta_beats_only.groupby(['user_idx', 'sample_idx'])['beat_prediction'].apply(
        lambda x: x.mode()[0]
    ).reset_index(name='segment_prediction')

    # Aggregate by Patient (60 seconds)
    patient_summary = segment_summary.groupby('user_idx')['segment_prediction'].apply(
        lambda x: x.mode()[0]
    ).reset_index(name='final_patient_diagnosis')

    return patient_summary, segment_summary

# Execution
if __name__ == "__main__":
    patient_results, segment_results = evaluate_ecg_patients(
        data_path="AR2026.03.csv",
        meta_path="cnn_ready_metadata_v4.csv",
        model_path="saved_model.pth" 
    )
    
    print("\n--- 10-Second Segment Diagnostics ---")
    print(segment_results)
    
    print("\n--- Overall Patient Diagnostics ---")
    print(patient_results)


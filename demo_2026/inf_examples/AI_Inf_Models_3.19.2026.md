# AI Inf Plan 3.2026  

... some other examples previous  

### Final example, full inference setup:  

```
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, List

WINDOW_SIZE = 250  
CLASS_NAMES = ['Normal (0)', 'Class 1', 'Class 2', 'Class 3', 'Class 4', 'Class 5', 'Class 6']

def extract_and_pad_heartbeat(signal: np.ndarray, peak_idx: int, window_size: int) -> np.ndarray:
    '''Extracts a peak-centered window and zero-pads if it hits the edge of the array.'''
    half_window = window_size // 2
    start_idx, end_idx = peak_idx - half_window, peak_idx + (window_size - half_window)
    pad_left, pad_right = max(0, -start_idx), max(0, end_idx - len(signal))
    
    beat = signal[max(0, start_idx):min(len(signal), end_idx)]
    if pad_left > 0 or pad_right > 0:
        beat = np.pad(beat, (pad_left, pad_right), mode='constant', constant_values=0.0)
    return beat

def run_inference(controller_csv: str, npy_dir: str, weights_path: str):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    df_control = pd.read_csv(controller_csv)
    npy_folder = Path(npy_dir)
    loaded_signals, results = {}, []

    for _, row in df_control.iterrows():
        file_name = row['filename'].replace('.hea', '.npy')
        lead_idx = int(row['lead_idx'])
        peak_pos = int(row['peak_position'])
        
        if file_name not in loaded_signals:
            file_path = npy_folder / file_name
            if not file_path.exists(): continue
            sig_array = np.load(file_path)
            if sig_array.shape[0] > sig_array.shape[1]: sig_array = sig_array.T
            loaded_signals[file_name] = sig_array
            
        signal = loaded_signals[file_name][lead_idx]
        beat = extract_and_pad_heartbeat(signal, peak_pos, WINDOW_SIZE)
        tensor_beat = torch.FloatTensor(beat).unsqueeze(0).unsqueeze(0).to(device)
        
        # MOCK INFERENCE 
        dummy_logits = torch.randn(1, len(CLASS_NAMES))
        probs = F.softmax(dummy_logits, dim=1).numpy()[0]
        
        result_dict = {'File': row['filename'], 'Lead': row['lead'], 'Beat_Idx': row['window_idx']}
        for i, class_name in enumerate(CLASS_NAMES):
            result_dict[class_name] = probs[i]
        results.append(result_dict)

    return pd.DataFrame(results)

def generate_report(df_results: pd.DataFrame):
    '''Aggregates heartbeat predictions and plots them.'''
    prob_columns = CLASS_NAMES
    df_summary = df_results.groupby('File')[prob_columns].mean().reset_index()
    
    df_display = df_summary.copy()
    for col in prob_columns:
        df_display[col] = df_display[col].apply(lambda x: f"{x * 100:.3f}%")
    
    print("\n" + "="*60 + "\n 🏥 ECG DIAGNOSTIC PREDICTION REPORT \n" + "="*60)
    print(df_display.to_string(index=False))
    
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")
    df_plot = df_summary.set_index('File')
    df_plot.plot(kind='bar', stacked=True, colormap='viridis', figsize=(10,6), width=0.7)
    plt.title('Diagnostic Class Probabilities per ECG Recording')
    plt.ylabel('Probability')
    plt.xlabel('Recording File')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()
```  





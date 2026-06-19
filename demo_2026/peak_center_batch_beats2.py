# Complex version with error checks 

import numpy as np
import scipy.io as sio
import scipy.signal as signal
import pandas as pd
import os

# Configuration
INPUT_FOLDER = "./data_mod_predict/"
OUTPUT_CSV = "cnn_ready_metadata_v4.csv"
DATASET = "AR2026.03.csv"   

BEAT_SIZE = 186
HALF_BEAT = BEAT_SIZE // 2
LEADS = ["I", "II", "V2", "V5"]

def process_all_files():
    all_rows = []
    all_beats = [] # Fixed: Initialize the list to hold the beat arrays
    
    if not os.path.exists(INPUT_FOLDER):
        print(f"Error: Folder {INPUT_FOLDER} not found.")
        return

    mat_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".mat")]
    
    for file_name in mat_files:
        mat_data = sio.loadmat(os.path.join(INPUT_FOLDER, file_name))
        val = mat_data['val']
        
        # Parse IDs safely
        parts = file_name.split('_')
        if len(parts) >= 2:
            u_idx = parts[0][1:]
            s_idx = parts[1][1:4]
        else:
            u_idx, s_idx = "Unknown", "Unknown"

        # Peak Detection on Lead II (Index 1)  
        peaks, _ = signal.find_peaks(val[1,:], distance=75, height=np.mean(val[1,:]))

        for win_idx, peak_pos in enumerate(peaks):
            
            # Extract for each lead
            # Fixed: Use enumerate to get an integer index (lead_idx) for the NumPy array
            for lead_idx, lead_name in enumerate(LEADS):
                
                # We want exactly 186 points. No need for a 250 window.
                win_start = peak_pos - HALF_BEAT
                win_end = peak_pos + (BEAT_SIZE - HALF_BEAT) 
                
                all_rows.append({
                    "filename": file_name,
                    "user_idx": u_idx,
                    "sample_idx": s_idx,
                    "lead_name": lead_name,
                    "window_idx": win_idx,
                    "peak_position": peak_pos,
                    "win_start": win_start,
                    "win_end": win_end
                })
                
                # Zero-filled array of exactly 186 shape
                beat = np.zeros(BEAT_SIZE) 
                
                # Boundary safety checks for beats right at the start or end of the file
                val_start = max(0, win_start)
                val_end = min(val.shape[1], win_end)
                
                beat_start = max(0, -win_start)
                beat_end = beat_start + (val_end - val_start)
                
                # Assign the slice
                beat[beat_start:beat_end] = val[lead_idx, val_start:val_end]
                all_beats.append(beat)
    
    # Export Metadata
    df = pd.DataFrame(all_rows)
    df.to_csv(OUTPUT_CSV, index=False)
    
    # Export Beats
    df2 = pd.DataFrame(all_beats)  
    df2.to_csv(DATASET, index=False, header=False) # header=False keeps the raw signal pure
    
    total_beats = len(all_beats) // len(LEADS)
    print(f"Success: Processed {len(mat_files)} files.")
    print(f"Total distinct heartbeat events identified: {total_beats}")
    print(f"Total signal rows extracted (all leads): {len(all_beats)}")
    print(f"Metadata saved to: {OUTPUT_CSV}")
    print(f"Heart beats dataset saved to: {DATASET}")

if __name__ == "__main__":
    process_all_files()

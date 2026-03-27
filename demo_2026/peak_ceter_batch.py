import numpy as np
import scipy.io as sio
import scipy.signal as signal
import pandas as pd
import os

# Configuration
WINDOW_SIZE = 250  
HALF_WINDOW = 125
INPUT_FOLDER = "./data_mod_predict/"
OUTPUT_CSV = "cnn_ready_predict_v3.csv"
LEADS = ["I", "II", "V2", "V5"]

def process_all_files():
    all_rows = []
    
    # Ensure directory exists
    if not os.path.exists(INPUT_FOLDER):
        print(f"Error: Folder {INPUT_FOLDER} not found.")
        return

    mat_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".mat")]
    
    for file_name in mat_files:
        # 1. Load Data (Expected shape: 4, 1250)
        mat_data = sio.loadmat(os.path.join(INPUT_FOLDER, file_name))
        val = mat_data['val']
        
        # 2. Parse IDs (U001_S002.mat -> 001, 002)
        u_idx = file_name.split('_')[0][1:]
        s_idx = file_name.split('_')[1][1:4]

        # 3. Peak Detection on Lead II (Index 1)
        # distance=75 at 125Hz ensures ~0.6s between beats
        peaks, _ = signal.find_peaks(val[1,:], distance=75, height=np.mean(val[1,:]))

        # 4. Create window metadata
        for win_idx, peak_pos in enumerate(peaks):
            # Calculate indices for the 250-sample window
            win_start = peak_pos - HALF_WINDOW
            win_end = peak_pos + HALF_WINDOW
            
            for lead_name in LEADS:
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
                
    # 5. Export to CSV
    df = pd.DataFrame(all_rows)
    df.to_csv(OUTPUT_CSV, index=False)
    
    total_beats = len(all_rows) // 4
    print(f"Success: Processed {len(mat_files)} files.")
    print(f"Total heart-beats identified: {total_beats}")
    print(f"Metadata saved to: {OUTPUT_CSV}")

if __name__ == "__main__":
    process_all_files()

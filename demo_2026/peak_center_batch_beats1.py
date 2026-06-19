# simplified version
# Gemini 6/19/2026 Friday 2:30pm, based on OpenAI mental block answer    

import numpy as np
import scipy.io as sio
import scipy.signal as signal
import pandas as pd
import os

# Configuration, removed window_size = 250, half_window = 125  
INPUT_FOLDER = "./data_mod_predict/"
OUTPUT_CSV = "cnn_ready_metadata_v4.csv"
DATASET = "AR2026.03.csv"
BEAT_SIZE = 186
HALF_BEAT = BEAT_SIZE // 2
LEADS = ["I", "II", "V2", "V5"]

all_rows = []
all_beats = []

# does not check for if directory exists.  
# not inside function definition, ok.  

for file_name in [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".mat")]:
    val = sio.loadmat(os.path.join(INPUT_FOLDER, file_name))['val']
    u_idx, s_idx = file_name.split('_')[0][1:], file_name.split('_')[1][1:4]
    
    # Peak detection on Lead II
    peaks, _ = signal.find_peaks(val[1,:], distance=75, height=np.mean(val[1,:]))
    
    for win_idx, peak in enumerate(peaks):
        for lead_idx, lead_name in enumerate(LEADS):
            # 1. Define exact 186 boundaries
            start = peak - HALF_BEAT
            end = peak + (BEAT_SIZE - HALF_BEAT)
            beat = np.zeros(BEAT_SIZE)
            
            # 2. Calculate safe boundaries for signals near the start/end of recordings 
            val_start, val_end = max(0, start), min(val.shape[1], end) # confused.
            beat_start = max(0, -start)
            beat_end = beat_start + (val_end - val_start) # don't know
            
            # 3. Extract and pad
            beat[beat_start:beat_end] = val[lead_idx, val_start:val_end]
            
            all_beats.append(beat)
            all_rows.append({
                "filename": file_name, "user_idx": u_idx, "sample_idx": s_idx,
                "lead_name": lead_name, "window_idx": win_idx, "peak_position": peak
            })

pd.DataFrame(all_rows).to_csv(OUTPUT_CSV, index=False)
pd.DataFrame(all_beats).to_csv(DATASET, index=False, header=False)

# Generally a cleaner execution. Not all calculations understood. Try run.  
# Works! Beats plotted. Centering is working, using II lead. 
# V2 and V5 looks off-center, but because the large peaks are static.  

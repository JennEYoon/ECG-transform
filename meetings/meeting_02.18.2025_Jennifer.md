# Meeting prep, Feb 18, 2025, by Jennifer Yoon  

### Review of datasets we have  

Over 60,000 unique patient data. All clean. Mostly in .mat (MATLAB) format. Chinese Shandong Provincial Hospital(SPH) is only dataset in a different format. This dataset downloaded separately from .tar compressed file.  

 * **Table, datasets**, over 60K:  
<img src="https://github.com/JennEYoon/ECG-transform/blob/main/notebooks/datasets_info/datasets_2021_table1.png" >

### PTB-XL dataset and sample notebook:    

#### PTB-XL Dataset Overview:   
Total files, 21,837  Storage: 2.58 GB disc space  
Format: .mat (MATLAB) and .hea (header) files for each recording  
Sampling rate: 500 samples per seconds, or 500 hertz.  
Length: 10 seconds. 
Leads: 12-leads, always in same order. (I, II, III, aVR, aVL, aVF, V1, V2, V3, V4, V5, V6) 
structure: array with shape (12 x 5000). 12 rows for 12 leads, 5000 columns for 10 seconds at 500 samples per second.  
Number of patients, sampling rate, data format etc.
   
#### Notebook for reading PTB-XL dataset, plotting figures:  

 1. notebook for loading .mat dataset, plotting.  PTB-XL few samples, 12-leads.    
https://github.com/JennEYoon/ECG-transform/blob/main/notebooks/load_mat.ipynb  

 2. figure large, 1st patinet, **all 12 leads, 10 seconds**  
<img src="https://github.com/JennEYoon/ECG-transform/blob/main/notebooks/ptb_sample/patient1_12lead.png"   >

 3. figure small, 1st patient, **few seconds and few leads**  
<img src="https://github.com/JennEYoon/ECG-transform/blob/main/notebooks/ptb_sample/ecg_4lead_4.5sec.png" width=500px  >

 4. figure small, **2nd patient**, few seconds and few leads
<img src="https://github.com/JennEYoon/ECG-transform/blob/main/notebooks/ptb_sample/HR00010_ecg4_4.5sec%20(2).png" width=500px >


JY comment: 
Heart beat signals seem to widen (various leads) for a time, then contract for a time (few seconds.) Same for both patients, HR00001 and HR00010. Is there autocorrelation among input leads? Some paper mention delay in reading from some of the leads (non-synchonous leads). Investigate. Also need to double check definition of lead placement. Some V's move with aVR/aVL or I, II, III leads. Verify location of leads in PTB XL study, Germany.  

Downsampling, Smoothing:  
Some paper smoothed ECG signal using cublic-spline. Does this help with AI modeling? Should I average signal to smooth? So far used 4th item select to downsample from 500 herts to 125 herts.      


### data splitting before training    

 1. Do a simple splitting notebooks using SciPy and Numpy.  

 2. copied notebook, ECG signal process and identify peaks: 

https://github.com/JennEYoon/ECG-transform/blob/main/notebooks/split_data/Pan_tompkins_%20step%20by%20step%20.ipynb  
 * Image, peaks identified on source
<img src="https://github.com/JennEYoon/ECG-transform/blob/main/notebooks/ptb_sample/ECG_peaks.png" > 

 3. If have time, website hosted Vis-App "live-feed" simulation.
    * Plotly and Voila
    * Embed in website (iframe, dynamic Plotly OK)  

Data fed in from URL hosted source.  
Initially data fed in from local file. Moving window, continuous update and every 5 second update options.  
Classification - every 3 second average, continuous updating and running total average.  





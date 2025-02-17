# Meeting prep, Feb 18, 2025, by Jennifer Yoon  

### Review of datasets we have  

Over 60,000 unique patient data. All clean. Mostly in .mat (MATLAB) format. Chinese Shandong Provincial Hospital(SPH) is only dataset in a different format. This dataset downloaded separately from .tar compressed file.  

 * **Table, datasets**, over 60K:  
<img src="https://github.com/JennEYoon/ECG-transform/blob/main/notebooks/datasets_info/datasets_2021_table1.png" >

### PTB-XL dataset discuss  

 * PTB-XL overvies:
Number of patients, sampling rate, data format etc.
   

 * notebook for loading .mat dataset, plotting.  PTB-XL few samples, 12-leads.    
https://github.com/JennEYoon/ECG-transform/blob/main/notebooks/load_mat.ipynb  

 * figure large, 1st patinet, **all 12 leads, 10 seconds**  
<img src="https://github.com/JennEYoon/ECG-transform/blob/main/notebooks/ptb_sample/patient1_12lead.png"   >


 * figure small, 1st patient, **few seconds and few leads**  
<img src="https://github.com/JennEYoon/ECG-transform/blob/main/notebooks/ptb_sample/ecg_4lead_4.5sec.png" width=500px  >


 * figure small, **2nd patient**, few seconds and few leads
<img src="https://github.com/JennEYoon/ECG-transform/blob/main/notebooks/ptb_sample/HR00010_ecg4_4.5sec%20(2).png" width=500px >


Figures comment: 
Heart beat signals seem to widen (various leads) for a time, then contract for a time (few seconds.) Same for both patients, HR00001 and HR00010. Also need to double check definition of lead placement. Some V's move with aVR/aVL or I, II, III leads. Verify location of leads in PTB XL study, Germany.  

Data downsampling comment:  
I've selected every 4th item to downsample data from 500 hetz to 125 hertz. I've seen cubic spline being used to get a smoother average data point. Maybe implement some averaging later? Does this help with AI training to have smoother curves?  

### data splitting  

Show notebook with key issues - copy  

Do a simple splitting notebooks using SciPy and Numpy.  

### if have time, Vis-App "live-feed" simulation  

Data fed in from URL hosted source.  
Initially data fed in from local file, fed 10-seconds at a time chunks.  
Classification - every 3 samples average, continuous updating and running average.  

Voila and Plotly  




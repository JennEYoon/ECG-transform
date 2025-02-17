# Meeting prep, Feb 18, 2025, by Jennifer Yoon  

### PTB-XL dataset discuss  

notebook for loading .mat dataset, plotting.  PTB-XL few samples, 12-leads.    
https://github.com/JennEYoon/ECG-transform/blob/main/notebooks/load_mat.ipynb  

> figure large, 1st patinet, all 12 leads, 10 seconds
> <img src="" width=600px >

> figure small, 1st patient, few seconds and few leads
> <img src="https://github.com/JennEYoon/ECG-transform/blob/main/notebooks/ptb_sample/ecg_4lead_4.5sec.png" width=500px >

> figure small, 2nd patient, few seconds and few leads
> <img src="https://github.com/JennEYoon/ECG-transform/blob/main/notebooks/ptb_sample/HR00010_ecg4_4.5sec%20(2).png" width=500px >


JY figures comment: 
Heart beat signals seem to widen (various leads) for a time, then contract for a time (few seconds.) Same for both patients, HR00001 and HR00010. Also need to double check definition of lead placement. Some V's move with aVR/aVL or I, II, III leads. Verify location of leads in PTB XL study, Germany.

### data splitting  

Show notebook with key issues - copy  

Do a simple splitting notebooks using SciPy and Numpy.  

### if have time, Vis-App "live-feed" simulation  

Data fed in from URL hosted source.  
Initially data fed in from local file, fed 10-seconds at a time chunks.  
Classification - every 3 samples average, continuous updating and running average.  

Voila and Plotly  




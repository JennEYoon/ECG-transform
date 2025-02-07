# PTB-XL dataset from Germany   
Author:  Jennifer Yoon  
Date:    Feb 5, 2025 Wednesday, 00:10 am  

#### Links:  
 * Jupyter Notebook: <a ref="https://github.com/JennEYoon/ECG-transform/blob/main/notebooks/load_mat.ipynb" >load_mat.ipynb link</a>  
   https://github.com/JennEYoon/ECG-transform/blob/main/notebooks/load_mat.ipynb  

 * Figures saved: <a ref="https://github.com/JennEYoon/ECG-transform/tree/main/notebooks/ptb_sample" >ptb_sample folder</a>  
   https://github.com/JennEYoon/ECG-transform/tree/main/notebooks/ptb_sample  

 * Google Drive, data folder: to be added  

#### Dataset Overview:   
Total files, 21,837  Storage: 2.58GB disc space  
Format: .mat (MATLAB) and .hea (header) files for each recording  
Sampling rate: 500 samples per seconds, or 500 hertz.  
Length: 10 seconds for files I looked at.  Are they all 10 seconds? To read paper to verify later.  
Mostly unique patients. A few many be repeated recordings of same patient. To verify num unique later.   
Grouped into folders, g1 to g22, with 1000 recordings per folder, mostly.  
Recording dates? To be filled in later. Maybe 2018-2020.   

Each datafile *.mat is a dictionary structure when read into Python. Has only one key: 'val' and only one value, one array object.  
Each array object is of shape (12 x 5000). (To verify later that all files are of same length). Rows are 12 leads. Columns are 5000 sampled points, at 500 samples per second. Time is 10 second length recording. Amplitude is in micro-Volts.  

Leads in order (always in same order): (I, II, III, aVR, aVL, aVF, V1, V2, V3, V4, V5, V6)  
Need to double check location of leads, as defined in Germany during recording. Some unexpected correlations between chest leads and limb leads and aVR, aVL, aVF leads.   

Source: Physionet 2020 CinC Challenge  
URL: https://physionetchallenges.github.io/2020/  
Title: ***Classification of 12-lead ECGs: The PhysioNet Computing in Cardiology Challenge 2020***  

#### Thoughts:  
Large dataset, 22K. Looks quite clean. When downsampled by taking every 4th data point, lines look jerky. To try smoothing by averaging over 4 samples instead of selected every 4th sample. Need to read source paper that described how the data was collected, and any deep learning models used by paper authors.  






# folder for splitting data  

ECG datasets are provided for 10-60 seconds at 500, 1000 hertz sampling rate. This folder will be used to test various ways to split the data into heatbeat sample for feeding into deep learning  models.  

I'm using PTB-XL as a first case. Will use 1.5 seconds and 125 hertz downsampled. Later may use cublic spline to average data in place of selecting every 4th data point, squaring to get rid of negative numbers, standardizing distance between peaks.  
 - Only filter now, low-pass filter for meandering low-volt around zero base. Feb 22, 2025.   

Huggingface may have pre-processed PTB-XL dataset, from ChatGPT. To investigate later.  
First use SciPy code to creat a simple script for splitting data into uniform segments. 
 - no, did not find useful pre-process PTB-XL on Huggingface.
   
Physionet Python library for processing ECG data (split, R-peak finding, noise reduction, filtering)  
https://wfdb.readthedocs.io/en/latest/  
Use later on. 


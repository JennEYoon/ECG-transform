# data_mod_predict folder contents  
Date: March 27, 2026 Friday  
Author: Jennifer Yoon

**Description:**    
ECG prototype recordings, modified for use in 1dcnn prediction model.  
Split into 10 second lengths, 125 hertz down sampled.   
Verified units millivolts, max +1.0 to min -1.0 range.  
4 channels, I, II, V2, V5, in that order.  
Each user has 6 data files, S000 to S005.    
Has 4 user files, U000 to U003.  
MatLab format .mat  
Data type 16 bit float.  

## todo 6/18/2026 9:15pm:   
Create csv file for model input   
[beat, 186]   
[beat, 186]   
format. Some columns before or after can have file id, channel id, diagnostic class info.  
Match .csv file for MIT-BIH exercise.   

### 6/23 TU  
Run 1dcnn inf model.  
Enlarge dataset, run using known abnormal classes from ptbxl.  
Create script to process more datasets. Run models on more datasets.  




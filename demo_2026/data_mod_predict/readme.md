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
Run ink using known abnormal classes from ptbxl. Like running test dataset, on a small sample.  
Create script to process more datasets. Run models on more datasets.  

After getting a model to run, need to refactor code to make it easy to maintain and understand. Also make batch processing easier.  

### July plan, next version simple ECG device  
Will be 12 channels. Get new device recordings in various lengths.  
Device output 100 ms, 0.01 sec.  
Need to be saged on a local computer to assemble into longer lengths.  
Later use cloud to assemble. Find out latency. Buffering and redunancy, Rebecca?  
Rebecca studying schematic for easy ECG device. Which chip?  

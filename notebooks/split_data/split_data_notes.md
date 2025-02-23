# Split Data  

Feb 22-23, 2025 WIP 
SciPy alone works pretty well for splitting samples into individual heart rate windows.  
Next, double check everything.  
Apply base low-voltage filter.  
Mark peaks on original data, show in plot.  

Come up with fast way to split a good sample data.  
Run both simple CNN and ECGTransform models.  
Verified today, ECGTransform split data into 1.5sec windows  
and fed 1 lead signal at a time.  

MIT-data, used 186 window size (sequence_length) 
2 leads, 5 classes, input_channels = 1 (one at a time)  
PTB-data, used 188, (186 windows, final 1-2 column is label)
input_channels = 1 (Again, one signal only at a time)  
class = 2 (normal, abnormal. ignored all sub classes)  



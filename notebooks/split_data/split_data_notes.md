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

March 1-2, 2025 notes:  
Each recording has 10-12 heart beat sample windows, when split into 1.5 sec x 125 herts (0-186) and center max peak, zero padding to left and right. These can be concatenated vertically. Each heart beat is fed into CNN model, ouput classification prediction for each hearbeat. All heartbeats will share same classification label from header file description.  

12-signals can be treated as 12-channels. Need to use one-hot encoding signal number identifier vector.  
Add lead ID vector after CNN training? Not sure how to do this. Bill idea.  

If leads are treated as a channel, can model it as another dimension in CNN.  
Each sample: uv y-axis, 187 time x-axis, 12-channel z-axis.  This is one heart beat.  
Next sample is same recording, 2nd heart-beat.  
Then after 10-12 heart beats,  
open next file and process the next set of 10-swcond recording.  

Number of samples from 100 recordings -> 1000 - 1200 sample heart beats, 12 channels, 186 time axis.  
Dim = (sample size x 186xuV x 120)  
Sample size can vary from 1000 to 1200, batch until end.  
voltage rescale to -1 to +1?  See how other papers did it.  

Lookup 12-signal papers from 2021 CinC challenge. How did they handle 12-signal data?  


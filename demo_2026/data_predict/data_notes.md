# ECG prototype device data  
Memo writer: Jennifer Yoon   
Files received from Ricardo on Friday, March 13, 2026.  

### About data files:  
 * 4 recordings from 4 males, age 25 three, age 26 one.  
 * date recorded: March 12, 2026 in Mexico. 
 * 4 ECG channels, limb I, limb II, V2, V5  
 * Diagnosis class, assumed all normal.  
 * 250 hertz, millivolts
 * Recording length about 10 seconds? Stated but not verified by me.  

### Update: March 18, 2026.  
Note .npy is the first collection from ARM chip (signals are in C code). 
This is then converted to .dat and .hea formats using "wfdb" Python library.  
May not need .dat file. Only seem to be used to rescale y-axis and change frequency to 250 hertz.  




# ECG prototype device data  
Memo writer: Jennifer Yoon   
Files received from Ricardo on Friday, March 13, 2026.  

### About data files:  
 * 4 recordings from 4 males, age 25 three, age 26 one.  
 * date recorded: March 12, 2026 in Mexico. 
 * 4 ECG channels, limb I, limb II, V2, V5  
 * Diagnosis class, assumed all normal.  
 * 250 hertz, millivolts
 * Recording length 60 seconds exactly, all four.
 * min -1.0 to max +1.0, float 16 bits.  

### Update: March 18, 2026.  
Note .npy is the first collection from ARM chip (signals are in C code). 
This is then converted to .dat and .hea formats using "wfdb" Python library.  
May not need .dat file. Only No difference w .npy data?  

### Comments on raw data:  
Limb I has many sharp spikes in down (negative) direction, that does not march w heart beat times. May need to sync slipts to Limb II or some other channel. V2 has baseline wonder that seems large. All channels have spikes and low waves. Seems like contact error and powerline interference. Baseline wonder is didd of Limb I and II leads not flattening out. Still, main signals surprisingly clear for first batch of real data from device.  

Examine .dat after processing by wsfd. What is different? Denoising filtering???   






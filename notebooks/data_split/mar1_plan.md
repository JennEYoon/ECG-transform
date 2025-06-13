# March 4, 2025 plan, data split task  

Two main ways to process 12-signal ECG data.  
1) Stage 1 - input 12-signals as a 3rd dimension (channels), similar to image processing, where 3rd dim is color (rgb).
   Better fit for simple CNN and ResNet based models  
2) Stage 1 - only use 2 dimensions, time and voltage. Broad encoding stage. Learn how to process signals by cutting up parts of signal into "tokens" (chunks).    
   In stage 2 - use 12-signals as filters and train a reiforcement model to fine tune encoding on 12-signals.
   Use one-hot encoding vector to identify 12-signals [1, 0, 0, ... 0]
   Better fit for Transformer based model.

Will need efficient way to process files.  
Dimension: PTB-XL one file is 10 seconds long at 500 hertz  
Downsampled to 125 hertz, 1.5 second segment is 187 points long.  
Each sample is [187 x uV], and each recording has 10-12 heart beats. 

Using 10 heart beats in 10 seconds: 
Sample dimensions [10 beats x 187 points/1.5 sec x 12 channels] using 3 dimensions  
Or [10 beats x 187 points] using 2 dimensions.  

Next recording will be concatenated along dimension 1.  
With 1000 recordings the size will be:  
[10000 beats x 187 points]  

All of PTB-XL is about 20,000 recordings, and at 10 seconds per recoring (assuming 10 heart beats)  
[200,000 x 187] with one-hot encoding later for 12-signals.  
At 3D [200,000 x 187 x 12]  

Need OS walk or other efficient way to handle large number of files.  
Also need to read ECG diagnosis info for header files *.hea that match data files *.mat.  

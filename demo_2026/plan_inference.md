# Plan, Brainstorm - Prediction Model, 1dcnn  

Date: March 18, 2026:  

### Gemini, Plans, Evaluate  
Various plans hashed out. I will use channel-agnostic 1dcnn with existing trained weights (.pth) file. This is trained on 12 channels, but is channel-agnostic. Uses 125 hertz, so convert inputs from 250 hertz to 125. Split input data into peak center and zero padding. Iterate through all files in the folder path.  

### Steps:  

 * Load .npy file, load .hea file.
 * Test file to make sure it's in usable format, data range is usable.
 * Rescale to 125 hertz, millivolts
 * Text processing .hea file for user ID, filename, channel name/id index.  
 * ***steps as of March 27, 2026 F*** 
> * Create .csv file with peak centering and file name + channel name for each signal. - done  
> * Inputs: controller .csv file, resampled input data files.- done  
> * Load .pth file (trained 1dcnn weights)
> * Run eval, produce table & plots, write to output file with prediction and probabilities.
 * Write message log - run-time success, error messages.
 * Save logs, model updates.  

### data connection points, call memo, March 27, 2026  
Jason and I decide to focus on **Firebase db** and Google AI stack for now.  
ECG device outputs data in 100 millisecond lengths (0.1 seconds). This can be set up to write directly to Google Cloud Firebase db account. Jason said he can convert raw binary/hex to float 16 data type before storing in Firebase db. Range: (-1.0 to +1.0).  

My Colab instance should be able to read directly from firebase db and execute the analysis, and write to firebase db, or other reports on webapp hosted on Full Stack Google environment. Uses node.js back end and React front end.  

Event handlers to start a Colab notebook, execute, write results.  
For abnormal heart-beats, based on on-chip edge-AI prediction, will start another event handler to run a 2nd model to verify abnormal heart-beats. No delay processing. Send warnings to user's phone.   

### March 28 and 29, Connection points   
AI edge, Firebase, MAX78000 chip specs, Google auth.  
12 hours.  

### April 28, 2026 TU 5pm.  Back to working on inference models.  
Next steps: create csv file with window size 186 long and 125 herts (downsample from 250 hertz) numpy data format.  
Run eval() using pre-trained model, weights. How to load pretrained model .pth?  
If necessary can re-train model.  
Run more diagnostics on eval().  

#### Next train on 2 more folders datasets, make sure results OK.  

#### Then try time-series using 1 folder, then 3 folders.  

#### After that is Edge-AI, 
 * Try train quantized aware, then  
 * Try post-train weights quantization and layer fusion.  

### June 5 F:  
call, plan 3.5h today.  
Need to get 1dcnn inference to work.  
Try loading a small sample abnormal files from ptbxl augmented.  
Then try 4 user recording. File already converter to .mat, 10 secs long, 125 herts, -1 to +1 volts range.  

### Inputs, Env, June 6, 2026 Saturday:  
Directory, inference data modified rescaled (data processing)  
Model structure, from training notebook - specify parameters (186 data columns, 187th is label, lead agnostic, batch size, training epochs) 
Controller peak centering csv file (data processing)  
Try using csv file for data to make it easier to run 1dcnn. Same as MIT dataset from Kaggle.   

Run first on PTBXL out of sample as inference data. Abnormal files select about 10 in all 5 categories.  
Next run Areteus ddevice output data. Code all as normal class.  
Try using csv files to make it easier, but matlab file format ok for now.  
Finish this weekend, Saturday and Sunday.  





...   

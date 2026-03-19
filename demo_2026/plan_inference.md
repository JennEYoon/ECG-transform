# Plan, Brainstorm - Prediction Model, 1dcnn  

Date: March 18, 2026:  

### Gemini, Plans, Evaluate  
Various plans hashed out. I will use channel-agnostic 1dcnn with existing trained weights (.pth) file. This is trained on 12 channels, but is channel-agnostic. Uses 125 hertz, so convert inputs from 250 hertz to 125. Split input data into peak center and zero padding. Iterate through all files in the folder path.  

### Steps:  

 * Load .npy file, load .hea file.
 * Test file to make sure it's in usable format, data range is usable.
 * Rescale to 125 hertz, millivolts
 * Text processing .hea file for user ID, filename, channel name/id index. 
 * Create .csv file with peak centering and file name + channel name for each signal.
 * Inputs: controller .csv file, resampled input data files.
 * Load .pth file (trained 1dcnn weights)
 * Run eval, produce table & plots, write to output file with prediction and probabilities.
 * Wrte message log - run-time success, error messages.
 * Save logs, model updates.  

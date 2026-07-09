# Work w Rebecca, Axel, get device data to GCS, then to Inference model on Vertex AI.  

### July 3-4, message w Rebecca, 1h   
Describe situation, Q& A.  

100 ms output 8 leads, 12 channel, JSON text format, float 16 numbers? amplitude range? 250 hertz sampling rate, continuous. How to break into heart beats for 1dcnn model? Where to do this processing, assembling 250 herts packets into minimum heart beat lengths? Rebeca to figure out w Axel. Me get ready to make it work from Vertex AI.  

### July 8th   
Messages w Rebecca, Axel. Plan 1h  
Think +2h  
Create sample files using Areteus march 2026 device recording and ptbxl augmented recordings abnormal classes.  
Chop into 1 second, 3 seconds, and 10 seconds segments. 
Data pre-processing, refactor to autodetect lengths. Have minimum length test.  
If valid, run process.  
Create 186 column csv data and meta data (user id, file id, peak location)  
Run inference, and group results by user. Minimum is one full heart beat.  
Process until end of feed. Timeout?  



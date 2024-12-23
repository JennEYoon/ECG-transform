# data  

### 0. ECGTransform pre-processed data, .pt format
PyTorch library
torch.save(x.pt), torch.load(x.pt)  
MIT - train.pt, test.pt, val.pt  79mb  
PTB - train.pt, test.pt, val.pt   10mb  

MIT data 5 classes, PTB data only 2 classes (N normal, M mal)  
Most training was done on MIT data, then generalized to PTB data,   
but PTB data is of much higher quality, 15 channels vs 2 channels, 
and measuring device is medical grade vs ambulatory (noisy).  

### 1. Kaggle, pre-processed, .csv format, MITBIH and PTB data   

https://www.kaggle.com/datasets/shayanfazeli/heartbeat/data  
https://www.kaggle.com/datasets/shayanfazeli/heartbeat  

Jennifer Yoon Google Drive share link:   
 * https://drive.google.com/drive/folders/10g2ykTyd34b3VZ_TBanyEUpubhPhqhKb?usp=sharing  

Info:  
 * csv format, from Kaggle, preprocessed, MIT and PTB sources, 125 Hertz downsampled, both sources.  Each row is a sample and is fixed width of 188 columns.  Last column is a classification label (1 is abnormal, 0 is normal).  Each sample is approximately 1.5 seconds long, usually starts at the beginning of a major pumping action.  Samples that are longer than 1.5 seconds are cropped, shorter samples are zero padded, to fix row length to 188.     

 * MIT 109,446 samples, 
   five label categories ['N': 0, 'S':1, 'V':2, 'F':3, 'Q':4]   
   (2 channels is source data, both apprear in Kaggle data?)  
 * PTB 14,552 samples, two classes, in separate files.  
   (Q. how many lead channels were kept???)

 * These samples are too far chopped into a 1.5 secon time frame, would be better to get a few comtinuous seconds on the PTB abnormal dataset.  Look at source data, unprocessed further by Kaggle.  Chopped ok for training base model, but PTB will ne difficult to classify into different arrythemias without lead id.  Whick of 12 leads are being shown?  

### 2. MIT BIH  
https://www.physionet.org/content/mitdb/1.0.0/

48 30-minute recordings from 2-channel ECG ambulatory 24-hour monitor (noisy), from 47 unique people.  
Recorded at BIH Lab (Beth Isreal Hospital), Boston 1975-79 period. Old tech, very old.  
Digitized to 360 samples per second, 11 bit resolution, 
2 physicians annotated each sample, clear up unreadable sections for computer to read.  

### 3. PTB
https://physionet.org/content/ptbdb/1.0.0/  

594 high resolution 15 lead ECG from 294 subjects, digitized to 1000 samples per second, recording dates 1990 - 1997, in Germany. Much better, newer tech, high precision measuring device.  
Used in 1995 paper, Germany.   

Original data downloaded, binary format except header file in text format.  
Try numpy to read binary numerical data, row at a time.  
OpenAI instructions saved.  

#### Waveform visualizer, PTB data source   
Leads: (i, ii, iii, avr, avl, avf), (v1, v2, v3, v4, v5, v6), (vx, vy, vz)  
<img src="ptb_sample/s003lre.jpg" width="600px" >  

### 4. Physionet/CinC Challenge 2017  
https://www.kaggle.com/datasets/luigisaetta/physionet2017ecg/data  

MatLab all formats, data, code.  .m format  
Single channel data. Contributed from a device manufacturer, name to add later.  
 * sample notebook, simply nn: https://www.kaggle.com/code/luigisaetta/ecgnotebookphy1-binary  

### 5. Other Kaggle, etc data sources  

Various notebooks at Kaggle provide links to pre-processed MIT and PTB source datasets, with different processing methods, sampled at different hertz, and mostly saved to .csv formats.  Some are binary file formats.  

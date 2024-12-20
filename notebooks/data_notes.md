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
 * csv format, from Kaggle, preprocessed, MIT and PTB sources, 125 Hertz downsampled, both sources, each sample is one heart beat, (centered using peaks, assumed), zero padded and cropped, fixed dimension to 188 items, last item in row is class label, each row is one sample.  

 * MIT 109,446 samples, 
   five label categories ['N': 0, 'S':1, 'V':2, 'F':3, 'Q':4]   
   (2 channels is source data, both apprear in Kaggle data?)  
 * PTB 14,552 samples, two classes, in separate files, not part of data.  
   (Q. how many lead channels were kept???)  

### 2. MIT BIH  
https://www.physionet.org/content/mitdb/1.0.0/

48 30-minute recordings from 2-channel ECG ambulatory 24-hour monitor (noisy), from 47 unique people.  
Recorded at BIH Lab (Beth Isreal Hospital), Boston 1975-79 period. Old tech, very old.  
Digitized to 360 samples per second, 11 bit resolution, 
2 physicians annotated each sample, clear up unreadable sections for computer to read.  


### 4. PTB
https://physionet.org/content/ptbdb/1.0.0/  

594 high resolution 15 lead ECG from 294 subjects, digitized to 1000 samples per second, recording dates 1990 - 1997, in Germany. Much better, newer tech, high precision measuring device.  
Used in 1995 paper, Germany.   

Original data downloaded, binary format except header file in text format.  

### 4. Physionet/CinC Challenge 2017  
https://www.kaggle.com/datasets/luigisaetta/physionet2017ecg/data  

MatLab all formats, data, code.  .m format  
Single channel data. 
 * sample notebook, simply nn: https://www.kaggle.com/code/luigisaetta/ecgnotebookphy1-binary  

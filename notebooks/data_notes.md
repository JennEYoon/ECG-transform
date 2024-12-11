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

### 1. MIT BIH  
https://www.physionet.org/content/mitdb/1.0.0/

48 30-minute recordings from 2-channel ECG ambulatory 24-hour monitor (noisy), from 47 unique people.  
Recorded at BIH Lab (Beth Isreal Hospital), Boston 1975-79 period. Old tech, very old.  
Digitized to 360 samples per second, 11 bit resolution, 
2 physicians annotated each sample, clear up unreadable sections for computer to read.  


### 2. PTB
594 high resolution 15 lead ECG from 294 subjects, digitized to 1000 samples per second, recording dates 1990 - 1997, in Germany. Much better, newer tech, high precision measuring device.  
Used in 1995 paper, Germany.   

Original data downloaded, binary format except header file in text format.  

### Physionet/CinC Challenge 2017  
MatLab all formats, data, code.  .m format  
Single channel data. 
 * .csv from kaggle: https://www.kaggle.com/datasets/luigisaetta/physionet2017ecg/data  
 * sample notebook, simply nn: https://www.kaggle.com/code/luigisaetta/ecgnotebookphy1-binary  

# data  

### 0. ECGTransform pre=processed data, .pt format
PyTorch library
torch.save(x.pt), torch.load(x.pt)  
MIT - train, test, validate  79mb  
PTB - train, test, validate   10mb  

### 1. MIT BIH
48 30-minute recordings from 2-channel ECG ambulatory 24-hour monitor (noisy), from 47 unique people.  
Recorded at BIH Lab (Beth Isreal Hospital), Boston 1975-79 period. Old tech, very old.  
Digitized to 360 samples per second, 11 bit resolution, 
2 physicians annotated each sample, clear up unreadable sections for computer to read.  


### 2. PTB
594 high resolution 15 lead ECG from 294 subjects, digitized to 1000 samples per second, 
Used in 1995 paper, Germany. Recording before then. When?  

### Physionet/CinC Challenge 2017  
MatLab all formats, data, code.  .m format  
Single channel data. 


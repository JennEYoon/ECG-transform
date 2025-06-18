# ResNet+SE model runs  

dl-ecg-classifier repo, main branch - SE+ResNet18 model.  

Model input parameter (12 x time)  1.5 sec at 125 hrtz? Original is 500 hz x 10 sec, 5000.  
ResNet+SE uses random cropping, 4096 samples at 256 hertz.  
Minimum hertz on datasets was 256. I can upsample to 500 or divide by 2 to get 250 hertz. Should be close enough.  

Ask AI to build from scratch a ResNet 34 model using 186 data points? Peak center 1.5 sec.  

model generation, claude 2 days

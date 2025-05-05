# AI for wearable ECG prototype 

Author: Jennifer E. Yoon   
Timeline: link to be added  
SciPy 2025: virtual poster presentation, July 9-11, 2025.  

### 1. Quick Project Description:  

This repo contains a deep learning project for a wearable, ECG prototype.   
Areteus (https://www.areteus.us/) is developing a novel wearable ECG (heart rate monitoring) device. It's novel factors are: (1) continuously wearable at home and (2) comparable to hospital machines (12 or more signals, high quality & low noise). This AI project will customize ECG classification model(s) for the Areteus device. A demo of final AI model will show live-feed ECG signals from the Areteus device, and sample diagnostic classifications using public datasets.  

### 2. Device Information:  

2.A) Areteus Device: See <a href="https://github.com/JennEYoon/ECG-transform/blob/main/_Wearable_ECG_Device.md" >_Wearable_ECG_Device.md</a>  
https://github.com/JennEYoon/ECG-transform/blob/main/_Wearable_ECG_Device.md

 * Device output data format: work in process.  
 * Alondra, April 2025 - Sample data file in hexadecimal, text file format.
   
2.B) hospital ECG devices  

2.C) at-home ECG devices  

 *** To write up introductory information about device. ***   

### 3. Stage 1: Literature and Public Datasets research:  

3.A) Review ECGTransform paper, original paper provided by Areteus:  
See a copy of author's repo: ECGTransForm folder.  

Datsets used:  
 * MIT dataset
 * PTB dataset

3.B) Research other ECG papers, training models, simpler models:    
 * Simple CNN
 * ResNet
 * RandomForest   

3.C) How to handle 12-leads, splitting data?: 
 * peak centering, baseline zero calibration  
 * ignore other filtering at this time (squaring to remove negative numbers, standardizing peak to peak distance)
 * library: wsfl - for ECG data processing, standarizing.
 * Also scikit-learn for testing my own splitting methods.   

 *** To write up Stage 1, parts A, B, C. Ready for write up. ***   

### 4. Stage 2: Deeper Literature and Datasets research, 12-leads models:  
Chinese datasets  
PTB-XL large dataset  
2020 Physionet CinC challenge 
 - datasets 
 - winning models & papers

 *** Currently here. To write current review of models, datasets. ***    

### 5. AI Model Customizing and Testing:    


### 6. Key Findings:  


### 7. App and Website Hosting, Report Writing:  

* documentation started
* organization started
* Embedding visualization (notebooks, plots) on website research
* Cloudflare - Flutter and Dart, AWS cloud hosting - quick reviews   
* Interactive python viz libraries (Plotly, Bokeh) research
* brainstorm data formats, uploading streaming data in packets, chunks, to hosted app/visualization.  



# AI models for wearable ECG prototype - quantified health

Author: Jennifer E. Yoon   
Timeline: link to be added  
SciPy 2025: virtual poster presentation, July 9-11, 2025.  

### 1. Quick Project Description:  

This repo contains a deep learning project for a wearable, ECG prototype.   
Areteus (https://www.areteus.us/) is developing a novel wearable ECG (heart rate monitoring) device. It's novel factors are: (1) continuously wearable at home and (2) comparable quality to hospital machines (12 or more signals, low noise). This AI project will customize ECG classification model(s) for the Areteus device. A demo of final AI model will show streaming diagnostic classifications using hospital datasets. Later, deploy app showing live signals from Areteus device(s) and continuously updated diagnostic classifications.  

### 2. Device Information:  

2.A) Areteus Device: See <a href="https://github.com/JennEYoon/ECG-transform/blob/main/_Wearable_ECG_Device.md" >_Wearable_ECG_Device.md</a>  
https://github.com/JennEYoon/ECG-transform/blob/main/_Wearable_ECG_Device.md

 * Device output data format: work in process.  
 * Alondra, April 2025 - Sample data file in hexadecimal, text file format.
 * Contact Alondra - get more samples, Areteus device, 10 seconds or longer.  
   
2.B) Hospital ECG devices  

2.C) Home-use ECG devices  

 *** To write up introductory information about device. ***   

### 3. Stage 1: Literature and Public Datasets Research:  

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

### 4. Stage 2: Deeper Literature and Datasets Research, 12-leads models:  

 * PTB-XL large dataset
 * SPH large dataset (Shandong Provincial Hospital)
 * Papers from 2020 and 2021 Physionet CinC challenges 
   - winning models & papers
   - datasets descriptions  

 *** Currently here. To write current review of models, datasets. ***    

### 5. AI Model Customizing and Testing:    


### 6. Key Findings:  


### 7. App and Website Hosting, Report Writing:  

* documentation started
* organization started
* Embedding visualization (notebooks, website, apps) - to research  
* Interactive python viz libraries (Plotly, Bokeh, Voila) - to research  
  \-\-\-  
* Areteus: Cloudflare - Flutter and Dart, AWS - AI model/app hosting - get overview   
* Areteus and me: Brainstorm data formats, uploading streaming data in packets or chunks, database schemas - to research


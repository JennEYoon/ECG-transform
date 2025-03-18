# ECG-transform repo, README.md  
Github: https://github.com/JennEYoon/ECG-transform/edit/main/README.md  

Author: Jennifer E Yoon   
Date Range: Nov 2024 - 2025

### 1. Quick Project Description:  

This repo contains a deep learning project for Areteus. (See https://www.areteus.us/)   
Areteus is developing a novel wearable ECG (heart rate signals) monitoring device. It's novel factors are: (1) continuously wearable at home and (2) comparable to hospital machines (12 or more signals). This AI project will customize ECG classification model(s) for Areteus's novel device. Visualization app showing live-feed ECG signals is also planned.  

### 2. Device Information:  

2.A) Areteus Device: See <a href="https://github.com/JennEYoon/ECG-transform/blob/main/_Wearable_ECG_Device.md" >_Wearable_ECG_Device.md</a>  
https://github.com/JennEYoon/ECG-transform/blob/main/_Wearable_ECG_Device.md

Device output data format: work in process. Sample data file.  

2.B) to write, hospital ECG devices  

2.C) at-home ECG devices  


### 3. Stage 1: Literature and Public Datasets research:  

3.A) Review ECGTransform paper, original paper provided by Areteus:  

See a copy of author's repo: ECGTransForm folder.  

Paper review, datasets review.  
* MIT dataset
* PTB dataset

3.B) Research other ECG papers, training models, simpler models:    
* Simple CNN
* ResNet
* RandomForest   

3.C) How to handle 12-leads, splitting data: 
* peak centering, baseline zero calibration  
* ignore other filtering at this time (squaring to remove negative numbers, standardizing peak to peak distance)
* library, wsfl - for ECG data processing, standarizing.  

### 4. Stage 2: Deeper Literature and Datasets research, 12-leads models:  
Chinese datasets  
PTB-XL large dataset  
2020 Physionet CinC challenge 
 - datasets 
 - winning models & papers

Currently here.  

### 5. AI Model Customizing and Testing:    



### 6. Key Findings:  


### 7. App and Website Hosting, Report Writing:  

* documentation started
* organization started
* Embedding visualization (notebooks, plots) on website research 
* Interactive python viz libraries research  

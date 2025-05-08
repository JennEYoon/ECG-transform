# AI models for wearable ECG prototype - quantified health

Author: Jennifer E. Yoon   
Timeline: <a href="_timeline.md" > _timeline.md </a>   
SciPy 2025 Conference: virtual poster presentation, July 9-11, 2025     

### 1. Quick Project Description:   

This repo contains a deep learning project for a wearable, ECG prototype.   
Areteus (https://www.areteus.us/) is developing a novel wearable ECG (heart rate monitoring) device. It's novel factors are: (1) continuously wearable at home and (2) comparable quality to hospital machines (12 or more signals, low noise). This AI project will customize ECG classification model(s) for the Areteus device. A demo of final AI model will show streaming diagnostic classifications using hospital datasets. Later, will deploy an app showing live signals from Areteus device(s) and continuously updated diagnostic classifications.  

### 2. Device Information:  

2.A) Areteus Device: <a href="https://github.com/JennEYoon/ECG-transform/blob/main/_Areteus_ECG_Device.md" >Areteus ECG device </a>.

 * Device output data format: work in process.  
 * Alondra, April 2025 - Sample data file in hexadecimal, text file format.
 * To get more samples, Areteus device, 10 seconds or longer - Alondra call.   
   
2.B) Hospital ECG devices  

2.C) Home-use ECG devices  

 *** To write up introductory information about device. ***   

### 3. Stage 1: Literature and Public Datasets Research:  

3.A) Review ECGTransform paper, original paper provided by Areteus.  
 * ECGTransForm Repo, authors'
 * paper
 * Datasets: MIT (link), PTB (link)  

3.B] Related papers and Jupyter notebooks, using MIT and PTB datasets.  
 * ResNet Kim et al. :
 * Another paper :  
 * Survey paper, historical: 
 * Simple CNN
 * Simple ResNet
 * RandomForest 

3.C) Data Processing Issues.   
How to make full use of 12-signals in PTB data? How to split raw data into samples? What filter or processing should be used? What Python libraries might be useful?:  

Data processing choices, after discussions with Areteus:  
   * Use only peak centering and baseline zero calibration for now.  
   * Ignore other filters at this time (e.g., squaring to remove negative numbers, standardizing peak to peak distance, standardizing peak amplitude across patients)   
   * library: wsfl - for ECG data processing, standarizing.   
   * library: scikit-learn - good enough for testing my own data splitting and filtering methods.   

 *** Ready for write up. ***   

### 4. Stage 2: Deeper Literature and Datasets Research, 12-signal models:  

Overview of new efforts to collect large 12-signal ECG datasets for use in AI models, from different hospitals in different countries. Attempts to unify ECG diagnostic classifications. Attempts to collect high quality signals from diverse populations.   

Selected large, 12-signal datasets:  
 * PTB-XL large dataset
 * SPH large dataset (Shandong Provincial Hospital)

Selected papers and notebooks:  
 * ResNet+SE paper: link  
   - Notebook implementation: my customization  
   - Dataset selection and processing choices:
 * Simple ResNet model for comparison:
   - ResNet34, 20-50 epochs, 12-signals treated as 12-channel input data.  
 * Transformers+RNN:
   - Notebook implementation:
   - Datasets (same as previous)
 * Original ECGTransform model for comparison, on large, 12-signal datasets.    
 * Simple CNN model on large datasets for comparison, 20-50 epochs     

 *** Currently here. To write as I go ***    

### 5. Device Signals Testing and AI Model Refinements:    


### 6. Key Findings:  


### 7. Deploy App on Cloud and Report Writing:  

* documentation - started
* organization - started
* Embedding visualization (notebooks, website, apps)    
* Interactive python viz libraries (Plotly, Bokeh, Voila)  
  \-\-\-  
* Areteus: Cloudflare - Flutter and Dart, AWS - AI model/app hosting - get overview   
* Areteus and me: Brainstorm data formats, uploading streaming data in packets or chunks, database schemas - to research



# AI for ECG prototype  

Author: Jennifer E. Yoon   
Timeline: <a href="_timeline.md" > _timeline.md </a>   
Company: Areteus (https://areteus.us/)   

### SciPy 2025 Conference: virtual poster presentation, July 9-11, 2025     
 * Title: AI for wearable ECG prototype - quantified health
 * Abstract: I will share my experience customizing AI models for a wearable ECG (electrocardiogram) prototype, including Transformers, ResNets, and Random Forests. While intended for data science students and practitioners, anyone interested in wearable devices or quantified health is welcome. Listeners will gain practical insights to apply in their own AI projects.  
Hospital-grade 12-signal ECG machines are bulky and expensive, while at-home devices capture only 1–6 asynchronous signals. The Areteus wearable ECG is designed for continuous home use, recording 12–19 synchronous signals. It is especially useful for detecting abnormal heartbeats during sleep and strenuous exercise.  
 * proposal: <a href="https://github.com/JennEYoon/ECG-transform/blob/main/SciPy2025-poster/application.md">application</a>  
 * conference: https://www.scipy2025.scipy.org/  
 * tags: #SciPy-2025  #ECG-prototype  #AI  #quantified-health  
 * Image: Areteus ECG, close-up of processing chip, V1, and V2 contacts.    
   <img src="https://github.com/JennEYoon/ECG-transform/blob/main/images/ECG-device-sm.png" width=300px alt="image of processing chip and v1 v2 electrodes" >  

### 1. Quick Project Description:   

This repo contains a deep learning project for a wearable, ECG prototype.   
Areteus (https://www.areteus.us/) is developing a novel wearable ECG (heart rate monitoring) device. It's novel factors are: (1) continuously wearable at home and (2) comparable quality to hospital machines (12 or more signals, low noise). This AI project will customize ECG classification model(s) for the Areteus device. A demo of final AI model will show streaming diagnostic classifications using hospital datasets. Later, will deploy an app showing live signals from Areteus device(s) and continuously updated diagnostic classifications.  

### 2. Device Information:  

2.A) Areteus ECG device: <a href="https://github.com/JennEYoon/ECG-transform/blob/main/_Areteus_ECG_Device.md" >Areteus ECG device </a>.

 * Device output data format: work in process.  
   - First file request, Alondra, single recording, 5 seconds long, hexadecimal format text file.
   - Second file request, Alondra, 30 recordings, 10 seconds long, hexadecimal and raw binary format text files.
   - To convert to compatible machine learning input format.  
   
2.B) Hospital ECG devices  

2.C) Home-use ECG devices  

 *** To write up introductory information about device. ***   

### 3. Stage 1: Literature and Public Datasets Research:  

3.A) Review original paper provided by Areteus.    
 * ECGTransForm paper: (https://www.sciencedirect.com/science/article/abs/pii/S1746809423011473)  
 * Repo: (https://github.com/emadeldeen24/ECGTransForm)
 * Datasets:
    - MIT-BIH (https://www.physionet.org/content/mitdb/1.0.0/)  
    - PTB (https://physionet.org/content/ptbdb/1.0.0/)  

3.B) Related papers and Jupyter notebooks, using MIT-BIH and PTB datasets.  
 * ResNet Kim et al. :
 * Another paper :  
 * Survey paper, historical: 
 * Simple CNN
 * Simple ResNet
 * Random Forest 

3.C) Data Processing Issues.   
How to make full use of 12-signals in PTB data? How to split raw data into samples? What filter or processing should be used? What Python libraries might be useful?:  

Data processing choices, after discussions with Areteus:  
   * Use only peak centering and baseline zero calibration for now.  
   * Ignore other filters at this time (e.g., squaring to remove negative numbers, standardizing peak to peak distance, standardizing peak amplitude across patients)   
   * library: wsfl - for ECG data processing, standarizing.   
   * library: scikit-learn - for testing my own data splitting and filtering methods.   

 *** Ready for write up. ***   

### 4. Stage 2: Deeper Literature and Datasets Research, 12-signal models:  

Overview of new efforts to collect large 12-signal ECG datasets for use in AI models, from different hospitals in different countries. Attempts to unify ECG diagnostic classifications. Attempts to collect high quality signals from diverse populations.   

Image: ECG signal leads positioning (chest: V1 to V6, limbs: I, II, III, AVL, AVR, AVF)  
Source: ECGPedia.org, part of CardioNetworks.org  
<img src="https://github.com/JennEYoon/ECG-transform/blob/main/images/chest_nodes_img.png" width=300px >

Chest lead description: 
V1 = 4th intercostal space right (IC4R), 
V2 = IC4L, V3=between V2 and V4, 
V4 = IC5 in midclavicular line, 
V5 = between V4 and V6, 
V6 = same height as V4 in axillary line. 
To register V4R, use V3 in the right mid-clavicular line.

Limb lead description:  to write  
I:  , II   , III   , AVR    , AVL    AVF = to foot  

Selected large, 12-signal datasets:  
 * PTB-XL large dataset (Physikalisch-Technische Bundesanstalt)
 * SPH large dataset (Shandong Provincial Hospital)

Selected papers and notebooks:  
 * ResNet+SE paper: Zhao et al
   - Too many layers, custom large kernals. Initially try simpler ResNet + few SE blocks.  
   - input to first convolutional layer is (12, 4096). 12-signals ARE input as 12-dim channel.  
   - used random splitting and zero padding, has overlaps. I will use peak centering without overlap, and zero padding.
   - 16 seconds, 257 hz. I will use 10 seconds and 125 Hz, PTB-XL (5000 hz, 10 sec).     
   - Reduce prediction classes from 24 to 2 and 6 classes. Get higher accuracy when using  simpler model architecture? When using less layers or more standard sized kernel filters (3x3 or 5x5)? The large expansion of classes from 2 or 6 in previous stage to 24 seems to decrease overall model accuracy even with much more complex architecture and heavy use of custom kernels.  
   - Notebook implementation: my customization  
   - Dataset selection and processing choices:
 * Simple ResNet model for comparison:
   - ResNet34, 20-50 epochs, 12-signals treated as 12-channel input data.  
 * Transformers+RNN:
   - Notebook implementation:
   - Datasets (same as previous)
 * Original ECGTransform model for comparison, on large, 12-signal datasets.    
 * Simple CNN model on large datasets for comparison, 20-50 epochs        

### 5. Key Findings:   


### 6. Device Signals Testing and AI Model Refinement:  


### 7. Deploy App on Cloud and Report Writing:  

 * documentation - started
 * organization - started
 * Embedding visualization (notebooks, website, apps) - to research     
 * Interactive python viz libraries (Plotly, Bokeh, Voila) - to research   



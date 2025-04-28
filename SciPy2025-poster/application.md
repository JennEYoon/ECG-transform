# SciPy 2025 application   
As of March 7, 2025 8:20am ET, edited  

## Proposal Title  
AI for wearable ECG prototype - quantified health

## Track (drop-down menu) 
Machine Learning, Data Science, Explainable AI  

## Abstract  
I will share my experience customizing AI models for a wearable ECG (electrocardiogram) prototype, including Transformers, ResNets, and Random Forests. While intended for data science students and practitioners, anyone interested in wearable devices or quantified health is welcome. Listeners will gain practical insights to apply in their own AI projects.  

Hospital-grade 12-signal ECG machines are bulky and expensive, while at-home devices capture only 1–6 asynchronous signals. The Areteus wearable ECG is designed for continuous home use, recording 12–19 synchronous signals. It is especially useful for detecting abnormal heartbeats during sleep and strenuous exercise.   
 
  * Github https://github.com/JennEYoon/ECG-transform  
  * Areteus (https://areteus.us/)

## Description (284 words)

### Customizing ECG Classification Models: A Data Science Journey   
This talk explores customizing ECG classification models for a wearable ECG prototype, focusing on deep learning models and dataset challenges. Like an adventure game, navigating this field required unlocking new knowledge at each stage.   
 
In November 2024, I spoke with my brother, Jason Yoon (Areteus), who had been developing a wearable ECG prototype for two years. With the hardware ready, he asked me to develop the AI component. He provided a research paper using Transformers and MIT-BIH and PTB datasets, dated October 2023.   
 
I began by replicating the paper’s results and investigating alternative models on Kaggle and Hugging Face. Surprisingly, simple CNNs and even Random Forests achieved similar accuracy. Examining data sources, I found that MIT-BIH, contained doctor-corrected signals, while PTB dataset, despite having 12-signals, were not leveraged. Also, these widely used datasets had limited patient numbers and diversity.   
 
### Key Questions Emerged:   
Would these models scale to larger, more diverse datasets? How would they handle 12–19 signals from Areteus’s ECG device?  
 
In January 2025, I discovered much larger 12-signal datasets from PhysioNet challenges with 60,000 to 80,000 patients. In February, I discovered many papers using 12-signal large datasets, all dated 2024. What a difference a year made! On these research papers, ResNets performed best, while Transformers remained strong. Transformers may be well suited for a two-stage training: first, learning signal patterns agnostic to signal identity, then refining the model by using one-hot encoding to separate by signal identity.  
 
### Impact & Next Steps:   
This project explored customizing AI models to classify ECG signals, by addressing dataset challenges and multi-signal modeling strategies. Future steps include continuing model refinement and deploying a streaming ECG classifier app.  

## Image:  
Areteus protototype ECG device, close0-up of chip, V1, and V2 contacts.    
<img src="https://github.com/JennEYoon/ECG-transform/blob/main/images/ECG-device-sm.png" width=200px >


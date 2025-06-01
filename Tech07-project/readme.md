# Stanford Continuing Education, Tech07 Spring 2025  
## Project: AI for Wearable ECG Prototype, ResNet+SE Model  

Jennifer E Yoon  
May 31, 2025  

 * Slides, 2 minute presentation: <a href="https://github.com/JennEYoon/ECG-transform/blob/main/Tech07-project/Jennifer_Yoon_slides_draft.pdf" alt="PDF slides, Tech07 Project">link - draft slide/a>  
    * Add 3 slides, why peak centering vs random cplitting, why ResNet SE - small hump in lesser V lead, swaped in channel pooling, why wearable device, some pre-existing conditions benefit from continuous monitoring at home, health enthu;siasts - quantified health, post workout heart recovery for peak athletic performance, cheaper alternatiev in poor contried, local clinic can filter conditions and recommend going to a big city for hopital ECG machine and doctors.
 * related article, ***Three Whys*** <a href="https://github.com/JennEYoon/ECG-transform/blob/main/Tech07-project/three_whys.md" >draft doc</a>- submit draft, to finish on Monday, 6/1/2025.   
 * Jupyter notebook, exploratory data analysis:- submit draft, to tweak and finish on Monday, 6/1/2025.  
   - one-two signal files, image signals from 12-leads. Patient header file format, strategy for extracting information. Histogram of dataset diagnostic distribution for PTB-XL (use study resource).
 * Jupyter notebook benchmarking: simple CNN model on small dataset (MIT-BIH)
 * Jupyter notebook benchmarking, Random Forest model on small dataset (MIT-BIH and/or PTB original)  
   \-\-\-  
 * Jupyter notebook, 12-signals ECG data file processing: < work in process >  
 * Jupyter notebook, header file processing: < work in process >  
 * Jupyter notebook, ResNet+SE model: < work in process, not finished >  

### Datasets:  
 * PTB-XL, new large dataset, 12-signals: 
 * MIT-BIT, older small dataset, 2-signals:  
 * PTB original, older small dataset, 12-signals:  

### Resources:  

ResNet:  
 * Deep Residual Networks, c. 2015: https://arxiv.org/abs/1512.03385
 * Yannic Kilcher:  https://www.youtube.com/watch?v=GWt6Fu05voI

SENet:  
 * Squeeze-and-Excitation (SE) Networks, c. 2017: https://arxiv.org/abs/1709.01507
 * Soroush Mehraban: https://youtu.be/3b7kMvrPZX8?si=g0JY09P5dIPMXwRj


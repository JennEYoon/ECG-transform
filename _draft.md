# draft, thoughts, notes  

Work in process, May 2025  


### 2. Device Information:  

 * Device output data format: work in process.  
 * Alondra, April 2025 - Sample data file in hexadecimal, text file format. A single 5 second recording. Verified header bytes info. Verified device output format.  
 * Alondra, May 2025 - 10 second long recordings, 30 in total, taken over 2 days. Half in hexadecimal, half in raw binary text files. Satisfies minimum sample size for Central Limit Theorum and Law of Large Numbers. Later, to expand subjects, some with known heart abnormalities.     

### 4. Stage 2: Deeper Literature and Datasets Research, 12-signal models:  

4.D) Selected papers and notebooks:  
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
    - Original ECGTransform model on PTB original dataset, with or without 12-channel depth.  
 * Simple CNN model on large datasets for comparison, 20-50 epochs        

### 7. Deploy App on Cloud and Report Writing:  

* documentation - started
* organization - started
* Embedding visualization (notebooks, website, apps)    
* Interactive python viz libraries (Plotly, Bokeh, Voila)  
  \-\-\-  
* Areteus: Cloudflare - Flutter and Dart, AWS - AI model/app hosting - get overview   
* Areteus and me: Brainstorm data formats, uploading streaming data in packets or chunks, database schemas - to research


### 5/19/2025 note:  
Removed ECGTransform repo copy. Keep copy locally.  
Updated main readme.md 5h  

# SciPy 2025, virtual poster submission  

### Title: AI for wearable ECG prototype - quantified health  
### Author: Jennnifer E Yoon  
### Online presentation during SciPy 2025 Conference, July 9-11, 2025.  

Poster proposal accepted, April 27, 2025  
 * Proceeding due June 6, 2025 Friday, only if writing an optional full article, max 6k words.
      
Plan to finish poster by June 30, 2025.  
Q&A slot to be assigned during July 9-11, 2025   
To record videos for poster presentation (5-minute, 30-minute, Q&A possible topics)
Final proceedings edit Oct 15, 2024. 

Read <a href="https://github.com/JennEYoon/ECG-transform/blob/main/SciPy2025-poster/application.md" > SciPy application </a>

### Poster Templates, Examples:  
 * Emailed SciPy organizers - vague on dates, format.  
 * Review 2024 Poster and Papers, Proceedings from SciPy 2024 Conference.  
 * SciPy 2022 rules, physical posters

### Github repo organization & visualization examples, formats:   



### Video examples, formats:  

 * short 5 minute overview
 * longer 30 minute talk
 * Q&A - possible questions, prepared with slides.      
 * Make sure I know ResNet+SE model really well. Compare w CNN.
   Does CNN fully connected layer have channel depth pooling?  

### Questions:  
  Q) How does the Areteus ECG device compare to hospital devices and other at-home devices? Potentially higher noise (from device and user movement)? Error from incorrect contact placement by user vs trained technician at hospital?  
  A) Hospital ECG machines automatically apply noise filtering before outputtting signals. Areteus ECG signal quality will be tested. Goal is to output signal quality that meets hospital machine quality.  
  A) Other at-home devices are not comparable. User usually holds the device in the hand and not move for 30 seconds. If the recording is unclear, user can re-record. A few 30-second recordings can be saved on the device. Signals are sent to a service provider, who employs technicians to read  the recordings (diagrams). A classification diagnosis is sent back to user. User must pay for a subscription fee that is separate from the device purchase price.  
  Q) Does 12-signal AI model require a totally different approach than 2-signal AI model? Explain.  
  A) More classes, much larger datasets, multiple hospitals. Dataset recording procedure and diagnostic classification labeling may differ systematically from hospital to hospital. About 15-20% loss of accuracy when applying a model trained in one hospital to dataset from a different hospital may happen.  

Issue) Areteus data samples small.  
If data noise is systematic in some way, try modifying public dataset in the same way, then I have many data to train for device.  
Even if noise is random from device, I may be able to introduce random noise to the public data, and use that to train.  
Inference, show running test on trained models. Right now only have 1 subject with healthy heart. Plan to get some abnormal heart readings. Hospitals? Friends with past heart attach or current heart condition?   

Issue) How to feed large number of data files for splitting and centering data into 1 heart beat per sample. Also add correct label to each sample. 

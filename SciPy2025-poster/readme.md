# SciPy 2025, virtual poster submission  

### Title: AI for wearable ECG prototype - quantified health  
### Author: Jennnifer E Yoon  
### Online presentation during SciPy 2025 Conference, July 9-11, 2025.  

Poster proposal accepted, April 27, 2025  
Plan to finish poster by June 30, 2025.  
Q&A slot to be assigned during July 9-11, 2025   
To record videos for poster presentation (5-minute, 30-minute, Q&A possible topics)   

Read <a href="https://github.com/JennEYoon/ECG-transform/blob/main/SciPy2025-poster/application.md" > SciPy application </a>

### Poster Templates, Examples:  




### Github repo organization & visualization examples, formats:   



### Video examples, formats:  

 * short 5 minute overview
 * longer 30 minute talk
 * Q&A - possible questions, prepared with slides.

### Questions:  
  Q) How does the Areteus ECG device compare to hospital devices and other at-home devices? Potentially higher noise (from device and user movement)? Error from incorrect contact placement by user vs trained technician at hospital?  
  A) Hospital ECG machines automatically apply noise filtering before outputtting signals. Areteus ECG signal quality will be tested. Goal is to output signal quality that meets hospital machine quality.  
  A) Other at-home devices are not comparable. User usually holds the device in the hand and not move for 30 seconds. If the recording is unclear, user can re-record. A few 30-second recordings can be saved on the device. Signals are sent to a service provider, who employs technicians to read  the recordings (diagrams). A classification diagnosis is sent back to user. User must pay for a subscription fee that is separate from the device purchase.  
  Q) Does 12-signal AI model require a totally different approach than 2-signal AI model? Explain.  
  A) More classes, much larger datasets, multiple hospitals. Dataset recording procedure and diagnostic classification labeling may differ systematically from hospital to hospital. About 15-20% loss of accuracy when applying a model trained in one hospital to dataset from a different hospital may happen.  



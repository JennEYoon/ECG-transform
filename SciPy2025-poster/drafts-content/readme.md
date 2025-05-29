# drafts of slides, content assets   



### Plan of Action  
 * Explore poster formats.
 * Get SciPy poster specs - emails sent 5/9/2025  
 * Develop ResNet+SE model nb portion
 * Areteus device output, reformat into numbers, arrays. Peak center, baseline zero.
   Run prediction. Analyze for noise, systematic errors.
   Augment public data to simulate Areteus output? Train model on augmented data?
   Need data from patients with different classes of abnormal heartbeats to test device.  
 * Write other parts, think about images
 * Add interactive graphs using Plotly, Bokeh, Voila.  
 * 3D heart simulation using 12-signal chest signals? Similar to geoseismic visualization for oil drilling?  Contrast healthy strong heart to a feeble low-blood volume heart? Does something like this already exist? Maybe for medical education? Appropriate for my use case?
 * baby heart simulation 3d, get baby hear rate public data sources, maybe on 2 signal? Helpful in Africa, poor countries, diagnose infant sudden death, heart abnormality in babies.
 * Jason called, try to get Areteus recordings from abnormal heart. Pharmay or Hospice near Pt Reyes. By July 1-4, latest, to include inference in SciPy poster.  

### Slide drafts, Images:  

Make 8-10 blocks  
 * overall metaphore - adventure game journey, small person going from scene to scene, sometimes climbing mountain.
 * Unlock knowledge at each level, solve problems at each stage, data issues, model issues, adopting to Areteus device?
 * 3D image of human toso wearing ECG device, w nodes. Imagined. Use ChatGPT image generation.  
 * sample heart rate, feature pattern
 * placement of 12 leads, diagram
 * data processing - filtering choices, diagram
 * contrast datasets earlier MIT, PTB, later large 12-lead.
 * model discussion, resnet simple and resnet+SE blocks
 * ECGTransform (only 2 class for PTB 12-signal data) vs Transformer+RNN
 * Simple CNN, and RandomForest models
 * Device signal processing, if any. Samples. Uploading streaming data to cloud.
 * Heart 3D image simulation, beating, adult healthy, vs senior abnormal, various classes
 * Baby heart beating 3D image simulatuion. Calm vs when Crying. Abnormal cases.  

### Squeeze and Excitation block  
https://youtu.be/3b7kMvrPZX8?si=OEYK6qrFtPrAg8uu  
paper:  https://arxiv.org/pdf/1709.01507  
2019  



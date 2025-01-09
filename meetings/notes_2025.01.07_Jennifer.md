# Meeting Notes, Jennifer Yoon  

January 7, 2025 call  

## Completed simple CNN model on MIT data, PTB data WIP   
Results very good with only a very simple 1D CNN model.  
Model is from Kaggle notebooks.  
Used .csv data, also from Kaggle. Pre-processed and resampled to 125 hz.  

Took 15 minutes to run on Colab T4 GPU 
10 epochs, batch size 64  
Training dataset accuracy 98.87% on last epoch.  
Test dataset accyract 98.43%, only slightly lower.  
  Jennifer note - maybe just running more epochs can lead to higher accuracy? Without using more complex models? Is overfitting a problem?  Augmented data a possible solution?  

These numbers are remarkably good for a very simple CNN model.  
Next working on PTB dataset - reformatted into .csv format and ready to try training.  

> See: https://github.com/JennEYoon/ECG-transform/blob/main/notebooks/ecg-1Dcnn_classifier.ipynb  

## Explored original paper dataset, *.pt PyTorch files  
Files only contain pre-processed datasets from PTB and MIT sources.  
Files do not contain any saved model weights.  
Files do not contain any saved model definitions or parameters, but source code have these info.  
Authors did not use any foundational model with pre-trained weights.  

After further review of the PDF paper and source code,  
it seems there is no need for saved model checkpoints, saved model weights, or foundational pre-trained model.  
The project is simple enough that none of these are needed.  

Ready to run the ECGTransform model using *.pt dataset files provided.  
PTB dataset *.pt files transformed into *.csv files for running on 1D CNN model above.   
> https://drive.google.com/drive/folders/1jOf2oLHqy5TZJlQHtxZr3ECUsCY662uY?usp=drive_link

> See: https://github.com/JennEYoon/ECG-transform/blob/main/notebooks/load_data_test_pt.ipynb  

## MLII lead definition found  
Re: MIT dataset  
Fist channel is mostly MLII, modified limb lead 2.
"The signal obtained from the modified lead II (MLII) ECG lead, which uses electrodes placed on the right arm and left leg, is the most commonly used signal in clinical practice for medical diagnosis. This lead provides a clear and consistent view of the electrical activity of the heart, particularly its rhythm, which is important for identifying both normal and abnormal heart functions in patients." Applsci 14 09307 g001, https://www.mdpi.com/2076-3417/14/20/9307

> See: https://github.com/JennEYoon/ECG-transform/blob/main/notebooks/data_notes.md   

## Ready for Device Data, When?  

Jason promised 5 minute recordings by Jan 7, 2025. Where is this?  
Also comparison to Hospital ECG data from Mexico?  

Added: Jason will look for Chinese ECG data files, thousands of samples, labeled arrythmia classes?  
   * Jason sent Chinese data possible link - WhatsApp. To follow up.
     
Added: Alondra will work on getting device recordings, right arm + left leg, plus any one chest aread lead.  
For 2 lead minimum (just like MIT dataset)  

Jennifer thinks, it may be helpful to do more broad research on ECG models, Jennifer only scratched the surface. Kaggle, YouTube. Many simple models available. 

       

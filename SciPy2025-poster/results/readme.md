# Results 1D-CNN 

Summary Table, Specificity, Sensitivity, Accuracy by class and by model.  

### Original Dataset  




### Augmented Dataset  

Evaluating model on test set...
Final Test Accuracy: 84.91%

==================================================
Per-Class Sensitivity and Specificity
==================================================
Class                               Sensitivity (Recall)      Specificity
--------------------------------------------------------------------------------
(0) Sinus Rhythm (Normal) (was class 0) 0.9316                    0.7471
(1) T-wave abnormal (was class 2)   0.5902                    0.9723
(2) Atrial Fibrillation (was class 3) 0.6469                    0.9855
(3) 1st degree AV block (was class 4) 0.7309                    0.9961
(4) Left anterior fascicular block (was class 5) 0.6889                    0.9817
(5) Other arrhythmias (was class 6) 0.7527                    0.9849
--------------------------------------------------------------------------------
OVERALL (Macro Avg)                 0.7235                    0.9446
==================================================

Classification Report (Sensitivity is 'recall'):
                                              precision    recall  f1-score   support

         Sinus Rhythm (Normal) (was class 0)       0.89      0.93      0.91     19963
               T-wave abnormal (was class 2)       0.73      0.59      0.65      3243
           Atrial Fibrillation (was class 3)       0.67      0.65      0.66      1263
           1st degree AV block (was class 4)       0.83      0.73      0.78       732
Left anterior fascicular block (was class 5)       0.73      0.69      0.71      1935
             Other arrhythmias (was class 6)       0.75      0.75      0.75      1601

                                    accuracy                           0.85     28737
                                   macro avg       0.77      0.72      0.74     28737
                                weighted avg       0.84      0.85      0.85     28737


# ChatGPT Data augmentation strategies  

PTB-XL first 1000 sample  

Main prompt:
Let's say you want to use a public 12-lead ECG dataset, like the more recent ones that have 100,000 patient results, to create training and test data for a ResNet + SE model to classify ten different types of heart conditions. But instead of hospital-style 12-signal measurements with conductive gel, the data comes from a prototype that has leads embedded into a elastic shirt. It's likely that there will be some displacement of each lead in the shirt from where the lead would be if placed using each patient's fiducials. Also, there will be added noise due to body & shirt movement.
How would you augment the public and test data to approximate the displacements and noise from the prototype. Would there be a much larger augmented dataset (using the public dataset as the basis)?



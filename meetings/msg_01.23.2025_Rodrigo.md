

[12:09 PM, 1/23/2025] Rodrigo Rosales: 
I was basically in the process of reading through the documentation of each dataset and check if it was possible to build a new data set with samples of multiple datasets to address class imbalance  
Also I found a python library that helps you process and analyze of physiological data  
  * "WFDB doc 4.2.0" :  https://wfdb.readthedocs.io/en/latest/
    - The native Python waveform-database (WFDB) package. A library of tools for reading, writing, and processing WFDB signals and annotations.  
  * https://physionet.org/content/wfdb/10.7.0/ 

[12:15 PM, 1/23/2025] Rodrigo Rosales: It should allow us to preprocess the data in its raw format and convert it into whatever format is convenient for further usage
[12:16 PM, 1/23/2025] Rodrigo Rosales: I'm uploading the datasets to google drive, each folder includes the .zip and a readme file with a brief description of the data and a link to the source or the dataset article as a pdf  

[12:20 PM, 1/23/2025] Rodrigo Rosales: the folder is called "12-lead datasets"
[12:20 PM, 1/23/2025] Rodrigo Rosales: some of them are pretty large
[12:22 PM, 1/23/2025] Rodrigo Rosales: I'd send the script I was working on to visualize the date but it's nots finished
[12:23 PM, 1/23/2025] Rodrigo Rosales: I think you'll be able to find some examples of how to work with the library I sent
[12:23 PM, 1/23/2025] Rodrigo Rosales: Most of the datasets store the ecgs on .dat or .mat file
[12:25 PM, 1/23/2025] Rodrigo Rosales: but with the library you target the .hea file and its linked to the respective .dat or .mat file  

[1:02 PM, 1/23/2025] Rodrigo Rosales: This Medium article is very short and simple but it kinda but it gives you an example to convert these files to cvd
[1:02 PM, 1/23/2025] Rodrigo Rosales: https://medium.com/@protobioengineering/how-to-get-heart-data-from-the-mit-bih-arrhythmia-database-e452d4bf7215


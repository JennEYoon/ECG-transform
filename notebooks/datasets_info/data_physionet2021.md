Data download is having issues -wget  
Wed Jan 29th.  
Try AWS s3 with url next  


Files
Total uncompressed size: 12.6 GB.

Access the files
Download the files using your terminal: wget -r -N -c -np https://physionet.org/files/challenge-2021/1.0.3/
Download the files using AWS command line tools: aws s3 sync --no-sign-request s3://physionet-open/challenge-2021/1.0.3/ DESTINATION  

Still downloading after 5-6 hours!  


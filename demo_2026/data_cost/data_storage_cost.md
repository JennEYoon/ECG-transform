# Google Data Storage cost

Region:  Mexico (northamerica-south1)  
Units/Time: per 1 gibibyte, per month   

 * Standard storage:  $0.026     $ 0.472 per user per month  
 * Nearline storage:  $0.018     $ 0.327
 * Coldline storage:  $0.006     $ 0.109  
 * Archive storage:   $0.0027    $ 0.049   
 * Rapid Cache store: $0.120012  $ 2.180  

### Device raw data storage estimate, per user, per month   

24 bit, 10 channels (12-signal ECG only), 250 herts (samples per sec)  
  = 60,000 bits per second  
  divide by 8 bits in a byte  
  = 7,600 bytes per second  
  
1 month = 60 sec x 60 min x 24 hours x 30 days = 2,592,000 seconds  
  x 7,600 bytes/sec = 19.440 gigabyte per month per user  
1 Gigibyte (2^30) ~ 1.07 Gigabyte (10^9)  

19.44 divide by 1.07 = ***18.168 gibibype per month per user***.  



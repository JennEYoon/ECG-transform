# Summary Data Flow, from Edge Device to Wifi to Firebase db (No USB).     
Date: April 3, 2026 Friday  
Author: Jennifer Yoon  
Reviewed with Jason Yoon   

### Device Onboarding (Wi-Fi Provisioning without Bluetooth)  
For initial demo units lacking Bluetooth, getting the device onto the user's home internet securely requires the SoftAP / Captive Portal method. This is the industry standard for headless IoT setup.  
 * Step 1 (SoftAP Mode): On boot, the MAX78000 acts as its own Wi-Fi router, broadcasting an SSID like ECG_Demo_Setup.
 * Step 2 (User Connects): The user connects their smartphone or computer to this setup network.
 * Step 3 (Captive Portal): The device intercepts the connection and automatically opens a local webpage on the user's screen (similar to hotel Wi-Fi logins).
 * Step 4 (Handshake): The user selects their home Wi-Fi network from a list and enters their password. The device saves these credentials, turns off its setup network, and connects to the internet to begin streaming.
 * Cons: cannot be connected continuously via wifi, webpage auto time-out, battery runs out on device.  

### Resources/Constraints, MAX78000 microcontroller:  
 * 512K Flash Memory (50-60% reserved for Edge-AI prediction model)  
 * But has Micro SD card connector, for more memory storage.
 * 100 millisecond sampling rate, data output is in binary

### Proposed data flow:  
 * Device samples 100 millisecond ecg sensor data in binary, and buffers 3.0 second chunks into local memory.  
 * All samples are timestamped. Streamed data can be out of order. Some fault tolerance and buffering during data stream.   
 * Device streams via Wifi connection (initially no Bluetooth) directly to Firebase Store db.
 * Authentication already handled via SoftAP when device was turned on (wifi connection)
 * Use Firebase Store (not real-time) to receive 3.0 second chunks in binary.
 * Firebase convert binary to float-16 (later may change to float-8), and scale to millivolts.
 * On Google Cloud, have event listener and event handler to call Vertex AI session.
 * Assemble necessary time-chunks and run AI model(s). This can be at Firebase or at Vertex AI end.
 * Results and charts sent to user's web page (or saved on device micro SD memory).
 * Note: Only Firebase Store is HIPPA compliant. Real-time Firebase stream is not.
 * Note2: 100 millisecond stream is too fast for Real-time Firebase or Firebase Store to handle. Some chuncking is needed. 1.5 second is our standard window size for one heart-beat in our AI models. 3.0 seconds gives us 2 full heart-beat windows. The 3.0 second window will usually contain 2-4 heart-beats.   

   



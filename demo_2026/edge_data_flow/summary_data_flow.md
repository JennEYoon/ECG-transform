# Summary Data Flow, from Edge Device to Wifi to Firebase db (No USB).     
Date: April 3, 2026 Friday  
Author: Jennifer Yoon

### Device Onboarding (Wi-Fi Provisioning without Bluetooth)  
For initial demo units lacking Bluetooth, getting the device onto the user's home internet securely requires the SoftAP / Captive Portal method. This is the industry standard for headless IoT setup.  
 * Step 1 (SoftAP Mode): On boot, the MAX78000 acts as its own Wi-Fi router, broadcasting an SSID like ECG_Demo_Setup.
 * Step 2 (User Connects): The user connects their smartphone or computer to this setup network.
 * Step 3 (Captive Portal): The device intercepts the connection and automatically opens a local webpage on the user's screen (similar to hotel Wi-Fi logins).
 * Step 4 (Handshake): The user selects their home Wi-Fi network from a list and enters their password. The device saves these credentials, turns off its setup network, and connects to the internet to begin streaming.
 * Cons: cannot be connected continuously via wifi, web auto time-out, battery runs out on device.  

### Resources/Constraints, MAX78000 microcontroller:  
 * 512K Flash Memory
 * But has Micro SD card connector, for more memory storage.
 * 100 millisecond sampling rate, data output, in binary

### Proposed data flow:  
 * Device samples 100 millisecond data outputs in binary, and buffers 1.5 to 3.0 seconds into local memory (15 to 30 samples)
 * Device converts binary to float on these stored samples (use calculation cycles)
 * Device streams via Wifi connection (initially no Bluetooth) directly to Firebase db.
 * Authentication already handled via SoftAP when device was turned on (wifi connection)
 * Use Firebase Store (not real-time) to receive 1.5 to 3.0 second chunks in float 16.
 * On Google Cloud, have event listener and event handler to call Vertex AI session.
 * Assemble necessary time-chunks and run AI model. This can be at Firebase or at Vertex AI end.
 * Results and charts sent to user's web page.
 * Note: Only Firebase Store is HIPPA compliant. Real-time Firebase stream is not.

   

 * 

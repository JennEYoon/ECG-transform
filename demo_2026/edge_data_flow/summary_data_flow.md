# Summary Data Flow, from Edge Device to Wifi to Firebase db on Google Cloud   
Date: April 3, 2026 Friday  
Author: Jennifer Yoon

### Device Onboarding (Wi-Fi Provisioning without Bluetooth)  
For initial demo units lacking Bluetooth, getting the device onto the user's home internet securely requires the SoftAP / Captive Portal method. This is the industry standard for headless IoT setup.  
 * Step 1 (SoftAP Mode): On boot, the MAX78000 acts as its own Wi-Fi router, broadcasting an SSID like ECG_Demo_Setup.
 * Step 2 (User Connects): The user connects their smartphone or computer to this setup network.
 * Step 3 (Captive Portal): The device intercepts the connection and automatically opens a local webpage on the user's screen (similar to hotel Wi-Fi logins).
 * Step 4 (Handshake): The user selects their home Wi-Fi network from a list and enters their password. The device saves these credentials, turns off its setup network, and connects to the internet to begin streaming.

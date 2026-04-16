User Question:  
What’s the easierst way for users?  We will be seding the device out to users for demo. We will not have access to user’s IP address or router wifi information. We can have instructions on finding the user’s wifi IP address in an instructions documentation. We want low tech people to be able to connect to the internet and try out the device.  

Gemini Reply:  
**Saturday, March 28, 2026 at 6:44 PM EDT**

Getting a headless Wi-Fi device (no screen, no keyboard) onto a user's home network without using Bluetooth is a classic IoT engineering challenge. It is the exact same problem the smart home industry (smart plugs, early Roombas, Chromecasts) had to solve years ago. 

Since you cannot pre-program their router's Wi-Fi name and password into the device, you must use a method called **SoftAP (Software Access Point) with a Captive Portal**. This is by far the easiest, industry-standard approach for non-technical users.

### The "Captive Portal" User Experience

Here is exactly what the user will do. It requires no IP addresses, no router settings, and no downloaded apps:

1.  **Power On:** The user plugs in the MAX78000. 
2.  **Connect to Device:** The instructions tell the user to open the Wi-Fi settings on their smartphone or laptop and look for a new network called **"ECG_Demo_Setup"**. They tap to connect to it.
3.  **The Pop-Up (Captive Portal):** As soon as they connect, their phone's operating system detects that this Wi-Fi has no internet. It automatically pops up a browser window (just like when you connect to public Wi-Fi at a hotel or airport).
4.  **Enter Credentials:** This pop-up is actually a tiny website hosted directly on the MAX78000 chip. The page displays a dropdown list of the Wi-Fi networks the chip can currently see. The user selects their home Wi-Fi and types their password.
5.  **Launch:** The user clicks "Save & Connect." The MAX78000 saves the password, shuts down its "Setup" Wi-Fi network, and permanently connects to the user's home router. The user can now open your web app gateway and start the demo.

*Note: If you have the budget for these demo units, the absolute "lowest-tech" zero-friction option is to mail them a cheap, pre-configured 4G/LTE mobile Wi-Fi hotspot in the box along with the chip. They just turn both devices on, and the chip connects automatically.*
  X No, Don't want to add to unit cost.  
  MicroSD card already adds $20 to cost.  

  

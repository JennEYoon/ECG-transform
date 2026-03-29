# cheap wifi dongle, sim card combo  

**Saturday, March 28, 2026 at 6:48 PM EDT**

If you want to completely eliminate the Wi-Fi setup friction for your demo users, sending a pre-configured hotspot in the box is the ultimate "plug-and-play" solution. 

For sending out demo units, you generally have two categories of cheap hotspots, plus the cost of the data plan:

### 1. 4G LTE USB Wi-Fi Dongles (Cheapest & Best for Demos)
These look like slightly oversized USB thumb drives. They do not have batteries; you simply plug them into a standard USB wall charger (which you can plug into the wall right next to the MAX78000). 
* **Cost:** Very cheap, usually between **$10 to $25**. 
* **Examples:** You will mostly find these as generic "Unlocked 4G LTE USB Dongles" on Amazon, Walmart, or eBay. ZTE (like the MF833V) and Huawei also make widely used versions. 
* **Why they are great:** Because they don't have a battery, they can't run out of charge and die halfway through a 3-day continuous ECG test. They just stay plugged into the wall and broadcast a dedicated Wi-Fi network that your Edge chip connects to.

### 2. Battery-Powered "Pocket" Hotspots
These are the standard, puck-shaped or rectangular devices that have their own rechargeable batteries. 
* **Cost:** Usually between **$30 to $50** if bought through a prepaid carrier, or **$50 to $80** fully unlocked. 
* **Examples:** * **Franklin T9 or T10:** Very popular, often around $40-$50.
    * **Moxee Mobile Hotspot:** Sold at Walmart for about $30 to $50 depending on the prepaid plan.
    * **EIOTCLUB M47:** Sells for about $80 fully unlocked and is specifically designed for IoT devices.
* **Why they are great:** They are completely wireless, which is perfect if your demo requires the user to walk around the house or travel while wearing the ECG monitor.

### The Missing Piece: The Data Plan (SIM Card)
The hotspot device itself requires a SIM card to connect to cellular towers. Because 10-second chunks of quantized ECG data only use a few kilobytes of data, your overall data usage will be incredibly low (likely less than 1GB for a whole month of testing). 

Instead of buying expensive $50/month smartphone plans, you should look into **IoT Data Plans** or cheap prepaid MVNOs (Mobile Virtual Network Operators):
* **EIOTCLUB:** Specifically sells IoT SIM cards. You can get 1GB of data valid for 30 days for about **$6 to $10**. 
* **Tello or Mint Mobile:** You can buy a basic 1GB or 2GB data-only SIM card for about **$5 to $10 a month**.

**The Setup:** You would buy the $15 USB dongle, pop a $5/month SIM card into it, pre-program the MAX78000 to look for the dongle's Wi-Fi name, and mail both devices to the user. All they have to do is plug them both into the wall!
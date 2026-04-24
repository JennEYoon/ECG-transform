# Max78000 notes  
By Jennifer Yoon, Aprl 24, 2026 Friday.  

Received in mail Wed. April 22, 2026. Cursory inspection. Chip seems complete, but no software disc or usb or even link to software. Lookup Youtube demo, find software to download. 


Found AMD software. Base chip is in C/C++ and needs to be compiled. DOES have Python converter to chip-aware C/C++. Recommend PyTorch (not TFLite) with chip. Built-in neural engine is optimized for PyTorch. Lots of learning to get up to speed! Start with demo, voiced numbers recognition, YouTube.   

> Gemini: Train your 1D CNN in PyTorch using the ai8x-training repository (link: https://github.com/analogdevicesinc/ai8x-training). This repo contains "wrappers" that ensure your model layers (convolution, activation, etc.) are compatible with the MAX78000 hardware.

> **YouTube Demo: Spoken Digit Recognition**
> Gemini: The demo you likely saw is the **Keyword Spotting (KWS)** example. It uses a CNN to recognize spoken words (like "one," "two," "stop," etc.) with ultra-low power.

* **Link to the Demo/Tutorial:** [Getting Started with MAX78000FTHR | YouTube](https://www.youtube.com/watch?v=h8WWK7p-jdU)  
* **Technical Deep Dive:** [Keyword Spotting using the MAX78000](https://www.analog.com/en/resources/design-notes/keywords-spotting-using-the-max78000.html)

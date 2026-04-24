Friday, April 24, 2026, 2:33 PM EDT

### **Where to Find Software & Drivers**

The primary development environment for the **MAX78000FTHR** is the **Analog Devices (formerly Maxim) Microcontroller SDK (MSDK)**. It is a comprehensive, Eclipse-based toolchain that includes everything needed to build, flash, and debug code on the ARM Cortex-M4 and RISC-V cores.

* **MSDK Repository:** [Analog-Devices-MSDK GitHub](https://github.com/Analog-Devices-MSDK/msdk)  
* **Documentation:** [MSDK User Guide](https://analog-devices-msdk.github.io/msdk/USERGUIDE/)  
* **What it includes:** Eclipse IDE, GCC toolchains (ARM and RISC-V), OpenOCD for debugging, and a vast library of examples specifically for the MAX78000.

### ---

**YouTube Demo: Spoken Digit Recognition**

The demo you likely saw is the **Keyword Spotting (KWS)** example. It uses a CNN to recognize spoken words (like "one," "two," "stop," etc.) with ultra-low power.

* **Link to the Demo/Tutorial:** [Getting Started with MAX78000FTHR | YouTube](https://www.youtube.com/watch?v=h8WWK7p-jdU)  
* **Technical Deep Dive:** [Keyword Spotting using the MAX78000](https://www.analog.com/en/resources/design-notes/keywords-spotting-using-the-max78000.html)

### ---

**Overview: 1D CNN for ECG on MAX78000**

To process ECG signals directly on the MAX78000FTHR, you will follow a specialized workflow that bridges your high-level Python models with the chip's hardware CNN accelerator.

| Phase | Description |
| :---- | :---- |
| **1\. Training** | Train your **1D CNN** in **PyTorch** using the [ai8x-training](https://github.com/analogdevicesinc/ai8x-training) repository. This repo contains "wrappers" that ensure your model layers (convolution, activation, etc.) are compatible with the MAX78000 hardware. |
| **2\. Quantization** | The MAX78000 uses **8-bit fixed-point** weights. You must perform **Quantization-Aware Training (QAT)** to maintain accuracy when moving from floating-point to 8-bit. |
| **3\. Synthesis** | Use the [ai8x-synthesis](https://github.com/analogdevicesinc/ai8x-synthesis) tool. This converts your quantized PyTorch checkpoint (.pth.tar) into optimized **C code** that manages the CNN hardware registers. |
| **4\. Firmware** | Integrate the generated C code into an MSDK project. Use the Arm Cortex-M4 to handle the ECG sensor input (via ADC or SPI/I2C) and feed the data into the CNN accelerator. |

### ---

**Hardware Connection & Languages**

* **Connection:** The board connects via a **Micro-USB cable**. It has an on-board **DAPLink** debugger, so your computer will recognize it as a serial device and a CMSIS-DAP debugger—no external hardware (like a J-Link) is required for basic programming.  
* **Languages:**  
  * **Model Development:** Python (PyTorch is the native and most supported path for this chip's synthesis tools).  
  * **Device Code:** **C/C++**. The synthesis tool "translates" your AI model into C, which you then compile using the MSDK.  
* **Note on TensorFlow Lite:** While the MAX78000 can technically run TFLite for Microcontrollers on its ARM core, you **must** use the Maxim/ADI PyTorch workflow to utilize the **CNN Accelerator**. Running TFLite on the CPU alone will be significantly slower and use much more power.

**Pro-Tip:** Since you are already working with ECG data and PyTorch, start by cloning the ai8x-training repo and looking at the **"Simple-KWS"** or **"MNIST"** examples. You can swap the 2D convolutions for 1D convolutions to suit your ECG time-series data.

Would you like a sample PyTorch model definition that is compatible with the MAX78000 hardware constraints?

https://www.youtube.com/watch?v=h8WWK7p-jdU  youTube link

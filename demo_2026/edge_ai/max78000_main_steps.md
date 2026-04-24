# MAX78000 docs, main steps

Keywords Spotting Using the MAX78000
Abstract
Audio assistants have become very popular with range of applications from household to automotive and industrial products and IoT. Such devices constantly listen to their surroundings and wake up on pretrained keywords to execute certain commands. Power consumption is a key factor for many of such resource constrained edge applications, where the connectivity to the cloud for processing of raw data is not feasibly. The MAX78000 is a new breed of Artificial Intelligence (AI) microcontroller built to enable neural networks to execute at ultra-low power and live at the edge of the IoT. In this document, we show case the implementation of a keyword spotting application on the MAX78000. The machine learning model is built with Maxim’s development flow on PyTorch, trained with a subset of Google’s speech command dataset with 20 keywords, and deployed on the MAX78000EVKIT.

Introduction
The application of digital assistants powered by voice-activated user interfaces has drastically increased in the recent years. While some products heavily rely on cloud connectivity to execute the speech recognition algorithms and natural language processing on powerful remote servers, it is not feasible in lower power devices to constantly stream the audio to the cloud for processing. Particularly, the detection of wake-up keywords as well as a limited set of command words are expected to be completed locally to optimize the power consumption and reduce the latency in IoT and edge applications. Such applications are efficiently covered by the MAX78000, an ultra-low power microcontroller with a Convolutional Neural Networks (CNN) accelerator.

CNNs are very popular in modeling acoustic systems, especially keyword detection. CNNs, like regular neural networks, are constructed as a series of neurons with weights and biases followed by a nonlinearity. However, a convolutional layer only looks into a local area with a fraction of the output neurons of the last layer at a time and slides it over the last layer per execution (Figure 1). A pooling layer is frequently used in tandem with the CNN to down sample the last layers output. Such operations are the heart of the MAX78000 CNN architecture employing 64 parallel processors, each with a pooling unit, a convolutional engine, and a dedicated weight memory.

This application note examines how to implement a keyword spotting application on the MAX78000, an ultra-low power microcontroller with a CNN accelerator. Twenty keywords were selected from the second version of the Google speech commands dataset to train the keyword spotting demonstration (KWS20).

Figure 1. Basic operation of the CNN.

Figure 1. Basic operation of the CNN.

MAX78000
The MAX78000 [1] is a new breed of Artificial Intelligence (AI) microcontroller built to enable neural networks to execute at ultra-low power and live at the edge of the IoT. This product combines the most energy-efficient AI processing with Maxim's proven ultra-low power microcontrollers. The hardware-based CNN accelerator enables battery-powered applications to execute AI inferences while spending only microjoules of energy. This makes it an ideal architecture for keyword spotting applications. The MAX78000 features an Arm® Cortex®-M4 with FPU CPU for efficient system control with an ultra-low-power deep neural network accelerator. Figure 2 shows the top-level architecture of the MAX78000.

Figure 2. The architecture of the MAX78000.

Figure 2. The architecture of the MAX78000.

The MAX78000 evaluation kit provides a platform to leverage the capabilities of the MAX78000 to build new generations of AI devices. The EV kit features onboard hardware like a digital microphone, serial port, camera module support, and a 3.5in touch-enabled color, thin-film transistor (TFT) display [2] (Figure 3) for the KWS20 demo application.

Figure 3. Keyword spotting demo on the MAX78000EVKIT.

Figure 3. Keyword spotting demo on the MAX78000EVKIT.

MAX78000 Development Flow
The PyTorch or TensorFlow-Keras toolchain can be used to develop a model for the MAX78000. The model is created with a series of defined subclasses representing the hardware. Some operations like pooling or activations are fused to 1D or 2D convolution layers, and fully connected layers. Rounding and clipping are also added to match the hardware.

The model is trained with floating-point weights and training data. Weights can be quantized either during training (quantization aware training) or after training (post-training quantization). The result of quantization can be evaluated over the evaluation dataset to check the accuracy degradation due to weight quantization.

The MAX78000 synthesizer tool (ai8xize) accepts the PyTorch checkpoint or TensorFlow exported ONNX files as an input, as well as the model description in the YAML format. A sample data file (.npy file) is provided to the synthesizer as well to verify the synthesized model on the hardware. The inference outcome for this data is compared with the expected output of the presynthesis model.

The MAX78000 synthesizer automatically generates the C code, which can be compiled and executed on the MAX78000. The C code includes Application Programming Interface (API) calls to load the weights as well as the provided sample data to the hardware to execute an inference on the sample data and compare the classification outcome with the expected result as a pass/fail sanity test. This generated C code can be used as an example to create own applications. Figure 4 shows the overall development flow of the MAX78000.

Figure 4. Development flow of the MAX78000.
<img src="fig4_dev_workflow.png" width=800px?
Figure 4. Development flow of the MAX78000.

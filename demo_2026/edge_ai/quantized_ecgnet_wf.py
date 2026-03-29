# quantized ecgnet wifi connection  
# reduce float32 weights to uint8  
# fuze layers to reduce total parameters to 300K  

import torch
import torch.nn as nn
import torch.optim as optim
import torch.ao.quantization as quant
from datetime import datetime

# --- 1. THE ADAPTED MODEL ARCHITECTURE ---
class QuantizedECGNet(nn.Module):
    def __init__(self, num_classes):
        super(QuantizedECGNet, self).__init__()
        
        # A. Add Stubs for float <-> int8 conversion
        self.quant = quant.QuantStub()
        self.dequant = quant.DeQuantStub()
        
        # B. Define ReLU as a module layer (Crucial for layer fusion)
        self.relu = nn.ReLU()
        
        # Layer 1: Reduced from 128 to 64 channels
        self.conv1 = nn.Conv1d(in_channels=1, out_channels=64, kernel_size=80, stride=4, padding=38)
        self.bn1 = nn.BatchNorm1d(64)
        self.maxpool1 = nn.MaxPool1d(kernel_size=3, stride=2, padding=1)
        
        # Layer 2: Adjusted input from 64 to 128 channels
        self.conv2 = nn.Conv1d(in_channels=64, out_channels=128, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm1d(128)
        self.maxpool2 = nn.MaxPool1d(kernel_size=3, stride=2, padding=1)
        
        # Layer 3: Kept at 256 channels
        self.conv3 = nn.Conv1d(in_channels=128, out_channels=256, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm1d(256)
        self.maxpool3 = nn.MaxPool1d(kernel_size=3, stride=2, padding=1)
        
        # Layer 4: Reduced from 512 to 256 channels to save massive memory
        self.conv4 = nn.Conv1d(in_channels=256, out_channels=256, kernel_size=3, padding=1)
        self.bn4 = nn.BatchNorm1d(256)
        self.maxpool4 = nn.MaxPool1d(kernel_size=3, stride=2, padding=1)
        
        # Output layer
        self.avgpool = nn.AdaptiveAvgPool1d(1)
        self.fc = nn.Linear(256, num_classes) # Adjusted input from 512 to 256
        self.log_softmax = nn.LogSoftmax(dim=1)

    def forward(self, x):
        # 1. Quantize incoming float32 data to uint8/int8
        x = self.quant(x)
        
        # 2. Replaced functional torch.relu with module self.relu
        x = self.maxpool1(self.relu(self.bn1(self.conv1(x))))
        x = self.maxpool2(self.relu(self.bn2(self.conv2(x))))
        x = self.maxpool3(self.relu(self.bn3(self.conv3(x))))
        x = self.maxpool4(self.relu(self.bn4(self.conv4(x))))
        
        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        
        # 3. Dequantize before Softmax (LogSoftmax works best in float32)
        x = self.dequant(x)
        x = self.log_softmax(x)
        return x

    def fuse_model(self):
        # C. Fuse sequential operations into single blocks for Edge AI speed
        quant.fuse_modules(self, [
            ['conv1', 'bn1', 'relu'],
            ['conv2', 'bn2', 'relu'],
            ['conv3', 'bn3', 'relu'],
            ['conv4', 'bn4', 'relu']
        ], inplace=True)


# --- EXAMPLES OF HOW TO APPLY THE WORKFLOWS ---

if __name__ == "__main__":
    num_classes = 5
    backend = 'qnnpack' # Standard backend for ARM/Edge/Mobile devices
    
    # =====================================================================
    # OPTION 1: POST-TRAINING QUANTIZATION (PTQ) - Fast, requires pre-trained model
    # =====================================================================
    print("--- Running Post-Training Quantization (PTQ) ---")
    
    # 1. Load your pre-trained float32 model
    ptq_model = QuantizedECGNet(num_classes)
    # ptq_model.load_state_dict(torch.load("my_pretrained_float32_weights.pth"))
    
    # 2. Set to eval mode and fuse layers
    ptq_model.eval()
    ptq_model.fuse_model()
    
    # 3. Apply the quantization configuration
    ptq_model.qconfig = quant.get_default_qconfig(backend)
    quant.prepare(ptq_model, inplace=True)
    
    # 4. Calibrate using a small batch of representative test data
    # (Simulating your dummy ECG data here: batch_size=32, channels=1, length=186)
    print("Calibrating...")
    dummy_calibration_data = torch.randn(32, 1, 186)
    with torch.no_grad():
        ptq_model(dummy_calibration_data)
        
    # 5. Convert to 8-bit integer model
    quantized_ptq_model = quant.convert(ptq_model, inplace=True)
    print("PTQ Conversion complete! Model is ready for the Edge chip.\n")
    
    
    # =====================================================================
    # OPTION 2: QUANTIZATION AWARE TRAINING (QAT) - Slower, high accuracy
    # =====================================================================
    print("--- Running Quantization-Aware Training (QAT) ---")
    
    # 1. Initialize a fresh model for training
    qat_model = QuantizedECGNet(num_classes)
    qat_model.train() # Must be in train mode
    
    # 2. Fuse layers BEFORE training begins
    qat_model.fuse_model()
    
    # 3. Apply the QAT specific configuration
    qat_model.qconfig = quant.get_default_qat_qconfig(backend)
    quant.prepare_qat(qat_model, inplace=True)
    
    # 4. Standard Training Loop (Simulated)
    optimizer = optim.Adam(qat_model.parameters(), lr=0.001)
    criterion = nn.NLLLoss()
    
    print("Simulating QAT training loop...")
    for epoch in range(2): # Usually requires fewer epochs than initial training
        # Here you would loop over your train_loader
        dummy_inputs = torch.randn(32, 1, 186)
        dummy_labels = torch.randint(0, num_classes, (32,))
        
        optimizer.zero_grad()
        outputs = qat_model(dummy_inputs)
        loss = criterion(outputs, dummy_labels)
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch+1} complete. Fake quantization applied.")
        
    # 5. Freeze statistics, set to eval, and convert to 8-bit
    qat_model.eval()
    quantized_qat_model = quant.convert(qat_model, inplace=True)
    print("QAT Conversion complete! Model is highly accurate and ready for Edge.")
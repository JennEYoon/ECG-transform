# Generic 1dcnn model architecture optimized for Analog Devices MAX78000
# ECG signals, expect (row, 186) input datasets. Peak centered window size 186.
# Channel sizes reduced to ensure the 8-bit weights fit within the 442 KB limit.

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
import torch.ao.quantization as quant
from datetime import datetime

# ==========================================
# 0. MOCK DATA SETUP (For demonstration)
# ==========================================
print("Generating dummy ECG data for demonstration...")
num_samples = 100
num_classes = 5

# Simulating (samples, channels, length) -> (100, 1, 186)
X_train_tensor = torch.randn(num_samples, 1, 186)
y_train_tensor = torch.randint(0, num_classes, (num_samples,))
X_test_tensor = torch.randn(20, 1, 186)
y_test_tensor = torch.randint(0, num_classes, (20,))

train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
test_dataset = TensorDataset(X_test_tensor, y_test_tensor)

train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)

# ==========================================
# 1. THE ADAPTED QUANTIZATION MODEL
# ==========================================
class QuantizedECGNet(nn.Module):
    def __init__(self, num_classes):
        super(QuantizedECGNet, self).__init__()
        
        # A. Quantization Stubs
        self.quant = quant.QuantStub()
        self.dequant = quant.DeQuantStub()
        
        # B. ReLU as a module (Required for fusing)
        self.relu = nn.ReLU()
        
        # Layer 1: Reduced to 64 channels
        self.conv1 = nn.Conv1d(in_channels=1, out_channels=64, kernel_size=80, stride=4, padding=38)
        self.bn1 = nn.BatchNorm1d(64)
        self.maxpool1 = nn.MaxPool1d(kernel_size=3, stride=2, padding=1)
        
        # Layer 2: 64 -> 128 channels
        self.conv2 = nn.Conv1d(in_channels=64, out_channels=128, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm1d(128)
        self.maxpool2 = nn.MaxPool1d(kernel_size=3, stride=2, padding=1)
        
        # Layer 3: 128 -> 256 channels
        self.conv3 = nn.Conv1d(in_channels=128, out_channels=256, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm1d(256)
        self.maxpool3 = nn.MaxPool1d(kernel_size=3, stride=2, padding=1)
        
        # Layer 4: Capped at 256 channels (Crucial for MAX78000 442KB limit)
        self.conv4 = nn.Conv1d(in_channels=256, out_channels=256, kernel_size=3, padding=1)
        self.bn4 = nn.BatchNorm1d(256)
        self.maxpool4 = nn.MaxPool1d(kernel_size=3, stride=2, padding=1)
        
        # Output layer
        self.avgpool = nn.AdaptiveAvgPool1d(1)
        self.fc = nn.Linear(256, num_classes) # Adjusted to 256 input features
        self.log_softmax = nn.LogSoftmax(dim=1)

    def forward(self, x):
        # Quantize inputs to int8
        x = self.quant(x)
        
        # Forward pass using module self.relu
        x = self.maxpool1(self.relu(self.bn1(self.conv1(x))))
        x = self.maxpool2(self.relu(self.bn2(self.conv2(x))))
        x = self.maxpool3(self.relu(self.bn3(self.conv3(x))))
        x = self.maxpool4(self.relu(self.bn4(self.conv4(x))))
        
        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        
        # Dequantize back to float32 BEFORE Softmax calculations
        x = self.dequant(x)
        x = self.log_softmax(x)
        return x

    def fuse_model(self):
        # Combine Convolution, BatchNorm, and ReLU into single operations
        quant.fuse_modules(self, [
            ['conv1', 'bn1', 'relu'],
            ['conv2', 'bn2', 'relu'],
            ['conv3', 'bn3', 'relu'],
            ['conv4', 'bn4', 'relu']
        ], inplace=True)

# ==========================================
# 2. TRAINING & CONVERSION WORKFLOWS
# ==========================================
if __name__ == "__main__":
    backend = 'qnnpack' # Best backend for edge devices like MAX78000
    
    # ---------------------------------------------------------
    # WORKFLOW A: POST-TRAINING QUANTIZATION (PTQ)
    # ---------------------------------------------------------
    print("\n" + "="*50)
    print("STARTING WORKFLOW A: POST-TRAINING QUANTIZATION")
    print("="*50)
    
    # Step 1: Initialize and train model standard float32 model
    ptq_model = QuantizedECGNet(num_classes)
    criterion = nn.NLLLoss()
    optimizer = optim.Adam(ptq_model.parameters(), lr=0.001)
    
    print("Training standard float32 model...")
    ptq_model.train()
    for epoch in range(2): # Shortened to 2 epochs for demo
        for inputs, labels in train_loader:
            optimizer.zero_grad()
            outputs = ptq_model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
    print("Float32 training complete.")
    
    # Step 2: Prepare for PTQ
    ptq_model.eval()
    ptq_model.fuse_model()
    ptq_model.qconfig = quant.get_default_qconfig(backend)
    quant.prepare(ptq_model, inplace=True)
    
    # Step 3: Calibrate with representative data
    print("Calibrating model for 8-bit scaling...")
    with torch.no_grad():
        for inputs, _ in train_loader:
            ptq_model(inputs) # Pass data through to record ranges
            
    # Step 4: Convert to uint8
    quantized_ptq_model = quant.convert(ptq_model, inplace=True)
    print("-> PTQ CONVERSION SUCCESSFUL. Model ready for synthesis.\n")


    # ---------------------------------------------------------
    # WORKFLOW B: QUANTIZATION AWARE TRAINING (QAT)
    # ---------------------------------------------------------
    print("\n" + "="*50)
    print("STARTING WORKFLOW B: QUANTIZATION-AWARE TRAINING")
    print("="*50)
    
    # Step 1: Initialize model
    qat_model = QuantizedECGNet(num_classes)
    qat_model.train()
    
    # Step 2: Fuse layers BEFORE training
    qat_model.fuse_model()
    
    # Step 3: Insert fake-quantization nodes
    qat_model.qconfig = quant.get_default_qat_qconfig(backend)
    quant.prepare_qat(qat_model, inplace=True)
    
    # Step 4: QAT Training Loop
    optimizer_qat = optim.Adam(qat_model.parameters(), lr=0.001)
    print("Training model with simulated 8-bit noise (QAT)...")
    for epoch in range(2): # Shortened to 2 epochs for demo
        for inputs, labels in train_loader:
            optimizer_qat.zero_grad()
            outputs = qat_model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer_qat.step()
    print("QAT training complete.")
            
    # Step 5: Convert to true uint8
    qat_model.eval()
    quantized_qat_model = quant.convert(qat_model, inplace=True)
    
    print("-> QAT CONVERSION SUCCESSFUL. Model ready for synthesis.\n")
    
    # The output models (quantized_ptq_model or quantized_qat_model) 
    # can now be saved via torch.save() and processed by the MAX78000 synthesis tool.

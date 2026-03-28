# Generic 1dcnn model architecture  
# ECG signals, expect (row, 186) input datasets. Peak centered window size 186, at 125 herts sampling rate. 
# labels on 187th column. 

# Define the model
class ECGNet(nn.Module):
    def __init__(self, num_classes):
        super(ECGNet, self).__init__()
        # Layer 1
        self.conv1 = nn.Conv1d(in_channels=1, out_channels=128, kernel_size=80, stride=4, padding=38)
        self.bn1 = nn.BatchNorm1d(128)
        self.maxpool1 = nn.MaxPool1d(kernel_size=3, stride=2, padding=1)  # Adjusted kernel size and stride
        # Layer 2
        self.conv2 = nn.Conv1d(in_channels=128, out_channels=128, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm1d(128)
        self.maxpool2 = nn.MaxPool1d(kernel_size=3, stride=2, padding=1)  # Adjusted kernel size and stride
        # Layer 3
        self.conv3 = nn.Conv1d(in_channels=128, out_channels=256, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm1d(256)
        self.maxpool3 = nn.MaxPool1d(kernel_size=3, stride=2, padding=1)  # Adjusted kernel size and stride
        # Layer 4
        self.conv4 = nn.Conv1d(in_channels=256, out_channels=512, kernel_size=3, padding=1)
        self.bn4 = nn.BatchNorm1d(512)
        self.maxpool4 = nn.MaxPool1d(kernel_size=3, stride=2, padding=1)  # Adjusted kernel size and stride
        # Output layer
        self.avgpool = nn.AdaptiveAvgPool1d(1)  # AdaptiveAvgPool1d to handle variable input lengths
        self.fc = nn.Linear(512, num_classes)
        self.log_softmax = nn.LogSoftmax(dim=1)

    def forward(self, x):
        # Layer 1
        x = self.maxpool1(self.bn1(torch.relu(self.conv1(x))))
        # Layer 2
        x = self.maxpool2(self.bn2(torch.relu(self.conv2(x))))
        # Layer 3
        x = self.maxpool3(self.bn3(torch.relu(self.conv3(x))))
        # Layer 4
        x = self.maxpool4(self.bn4(torch.relu(self.conv4(x))))
        # Output layer
        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        x = self.log_softmax(x)
        return x

# Instantiate the model
num_classes = 5  # Change to the actual number of classes in your dataset
model = ECGNet(num_classes)
# Define loss function and optimizer
criterion = nn.NLLLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

print("Model defined and initiated.")
print(type(ECGNet), type(model))


# Training the model
num_epochs = 10
start_time = datetime.now()  # datetime library
for epoch in range(num_epochs):
    model.train()
    train_loss = 0.0
    correct = 0
    total = 0
    for inputs, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
    train_accuracy = 100 * correct / total
    print(f'Epoch [{epoch+1}/{num_epochs}], Train Loss: {train_loss:.4f}, Train Accuracy: {train_accuracy:.2f}%')
end_time = datetime.now()
print("\nTotal training time: {}".format(end_time - start_time))


# Evaluation on test set
model.eval()
test_loss = 0.0
correct = 0
total = 0
with torch.no_grad():
    for inputs, labels in test_loader:
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        test_loss += loss.item()
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

test_accuracy = 100 * correct / total
print(f'Test Loss: {test_loss:.4f}, Test Accuracy: {test_accuracy:.2f}%')




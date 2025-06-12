import os
import numpy as np
import torch
from torch.utils.data import Dataset

# Augmentation functions (from previous implementation)
def add_gaussian_noise(signal, noise_level=0.01):
    noise = np.random.normal(0, noise_level, signal.shape)
    return signal + noise

def add_baseline_wander(signal, freq=0.3, amplitude=0.05, fs=500):
    t = np.arange(signal.shape[1]) / fs
    wander = amplitude * np.sin(2 * np.pi * freq * t)
    return signal + wander[np.newaxis, :]

def add_emg_noise(signal, burst_duration=0.2, burst_freq=50, fs=500):
    burst_length = int(burst_duration * fs)
    start = np.random.randint(0, signal.shape[1] - burst_length)
    burst = np.random.normal(0, 0.1, (signal.shape[0], burst_length)) * np.sin(2 * np.pi * burst_freq * np.arange(burst_length) / fs)
    noisy_signal = signal.copy()
    noisy_signal[:, start:start + burst_length] += burst
    return noisy_signal

def lead_dropout(signal, dropout_prob=0.2):
    dropped_signal = signal.copy()
    for i in range(signal.shape[0]):
        if np.random.rand() < dropout_prob:
            dropped_signal[i, :] = 0
    return dropped_signal

def time_warp(signal, max_warp=0.1):
    from scipy.interpolate import interp1d
    original_length = signal.shape[1]
    warp = np.random.uniform(-max_warp, max_warp)
    warp_index = np.linspace(0, original_length, original_length)
    stretched_index = np.linspace(0, original_length, int(original_length * (1 + warp)))
    warped_signal = np.zeros((signal.shape[0], len(stretched_index)))
    for i in range(signal.shape[0]):
        f = interp1d(warp_index, signal[i, :], kind='linear', fill_value="extrapolate")
        warped_signal[i, :] = f(stretched_index)
    warped_signal = torch.tensor(warped_signal, dtype=torch.float32)
    warped_signal = torch.nn.functional.interpolate(warped_signal.unsqueeze(0), size=original_length, mode='linear', align_corners=False).squeeze(0).numpy()
    return warped_signal

def amplitude_scaling(signal, scale_range=(0.9, 1.1)):
    scales = np.random.uniform(scale_range[0], scale_range[1], signal.shape[0])
    return signal * scales[:, np.newaxis]

def augment_ecg(signal, fs=500):
    signal = add_gaussian_noise(signal)
    signal = add_baseline_wander(signal, fs=fs)
    signal = add_emg_noise(signal, fs=fs)
    signal = lead_dropout(signal)
    signal = time_warp(signal)
    signal = amplitude_scaling(signal)
    return signal

# ECG Dataset Class
class AugmentedECGDataset(Dataset):
    def __init__(self, ecg_data, labels, fs=500, augment=True):
        """
        ecg_data: numpy array of shape (N, 12, T)
        labels: numpy array of shape (N,)
        fs: sampling frequency (Hz)
        augment: apply augmentation if True
        """
        self.ecg_data = ecg_data
        self.labels = labels
        self.fs = fs
        self.augment = augment

    def __len__(self):
        return len(self.ecg_data)

    def __getitem__(self, idx):
        signal = self.ecg_data[idx]
        label = self.labels[idx]
        if self.augment:
            signal = augment_ecg(signal, fs=self.fs)
        signal = torch.tensor(signal, dtype=torch.float32)
        label = torch.tensor(label, dtype=torch.long)
        return signal, label


To train a robust ResNet + SE model for classifying ECG signals from a wearable shirt-based ECG prototype, while using hospital-style 12-lead ECG datasets like PTB-XL and SPH, the goal is to bridge the gap between clean, clinical ECG signals and noisy, displaced prototype signals. Since you have limited data from your prototype but ample hospital ECG data, data augmentation is essential. Here's a strategy to simulate your prototype conditions and generate a much larger augmented dataset from the public datasets:

### 1. **Displacement Simulation**

Displacement of leads due to elastic shirt fit and patient movement affects spatial orientation of electrical signals. Simulate this by:

* **Lead mixing**: Apply small linear combinations of adjacent leads (e.g., aVL, I, and V5) to mimic spatial blurring.
* **Random affine transformations**: Treat 12-lead ECG as a 2D signal grid (although it's not spatially laid out) and apply transformations that simulate lead shifts.
* **Reweighting lead contributions**: Modulate amplitude of each lead randomly within physiologically plausible limits (e.g., 90% to 110%) to reflect changes in electrode-skin coupling.

### 2. **Noise Injection**

To replicate prototype noise due to motion, loose contact, or non-gel electrodes:

* **Gaussian noise**: Add low-level Gaussian noise to simulate electronic noise.
* **Baseline wander**: Add low-frequency components (e.g., 0.2-0.5 Hz sine waves) to mimic respiration artifacts.
* **Muscle noise (EMG-like bursts)**: Inject short bursts of high-frequency noise (20–100 Hz) randomly.
* **Movement artifacts**: Introduce signal dropouts or amplitude spikes in random leads for short intervals.

### 3. **Signal Warping**

To model physical deformation effects:

* **Time warping**: Slight non-linear stretching/compression of the signal to reflect inconsistent sampling due to movement.
* **Amplitude scaling**: Random fluctuations in gain per beat or segment.
* **ECG morphology morphing**: Apply small shape transformations on QRS, P, and T waves to simulate electrode displacement.

### 4. **Domain-Specific Augmentations**

* **Heart rate variation**: Adjust RR intervals within physiological ranges.
* **Lead dropout simulation**: Randomly zero out one or more leads temporarily.

### 5. **Use Sim2Real Transfer Learning**

After augmenting hospital ECG data:

* Pre-train your ResNet + SE model on this large, diverse augmented dataset.
* Fine-tune on your limited prototype data with techniques like:

  * Gradual unfreezing of network layers
  * Lower learning rate
  * Loss weighting to emphasize prototype data

### 6. **Amount of Augmentation**

Yes, you would create a much larger augmented dataset. Common ratios:

* For each real ECG recording, generate 5–20 augmented variants, depending on the diversity of transformations.
* Consider using augmentation pipelines (e.g., via PyTorch, TensorFlow, or the `tsaug` or `numenta/htm.core` libraries).

### PyTorch + NumPy Implementation

```python
import numpy as np
import torch

# Gaussian noise
def add_gaussian_noise(signal, noise_level=0.01):
    noise = np.random.normal(0, noise_level, signal.shape)
    return signal + noise

# Baseline wander
def add_baseline_wander(signal, freq=0.3, amplitude=0.05, fs=500):
    t = np.arange(signal.shape[1]) / fs
    wander = amplitude * np.sin(2 * np.pi * freq * t)
    return signal + wander[np.newaxis, :]

# EMG noise bursts
def add_emg_noise(signal, burst_duration=0.2, burst_freq=50, fs=500):
    burst_length = int(burst_duration * fs)
    start = np.random.randint(0, signal.shape[1] - burst_length)
    burst = np.random.normal(0, 0.1, (signal.shape[0], burst_length)) * np.sin(2 * np.pi * burst_freq * np.arange(burst_length) / fs)
    noisy_signal = signal.copy()
    noisy_signal[:, start:start + burst_length] += burst
    return noisy_signal

# Lead dropout
def lead_dropout(signal, dropout_prob=0.2):
    dropped_signal = signal.copy()
    for i in range(signal.shape[0]):
        if np.random.rand() < dropout_prob:
            dropped_signal[i, :] = 0
    return dropped_signal

# Time warping
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

# Amplitude scaling
def amplitude_scaling(signal, scale_range=(0.9, 1.1)):
    scales = np.random.uniform(scale_range[0], scale_range[1], signal.shape[0])
    return signal * scales[:, np.newaxis]

# Apply full augmentation pipeline
def augment_ecg(signal, fs=500):
    signal = add_gaussian_noise(signal)
    signal = add_baseline_wander(signal, fs=fs)
    signal = add_emg_noise(signal, fs=fs)
    signal = lead_dropout(signal)
    signal = time_warp(signal)
    signal = amplitude_scaling(signal)
    return signal
```

### Summary

With these augmentations, you're effectively simulating the domain shift from hospital to wearable ECG, and generating a larger, richer dataset for training. This approach should allow your model to learn invariant features that transfer well to the prototype signals, even with minimal real training data from your device.





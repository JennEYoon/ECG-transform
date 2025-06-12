import numpy as np
import torch
import torch.nn.functional as F
from scipy.interpolate import interp1d
from typing import Tuple, Optional
import matplotlib.pyplot as plt

class SpatialTransformations:
    """
    ECG Spatial Transformations for simulating lead displacement in wearable devices.
    Implements rotations, time-domain scaling, inter-lead delays, and amplitude scaling.
    """
    
    def __init__(self, sampling_rate: int = 500):
        """
        Initialize spatial transformations.
        
        Args:
            sampling_rate (int): ECG sampling rate in Hz
        """
        self.sampling_rate = sampling_rate
    
    def apply_rotation(self, ecg_signal: np.ndarray, rotation_angle: float) -> np.ndarray:
        """
        Apply rotation transformation to simulate electrode displacement.
        
        Args:
            ecg_signal (np.ndarray): ECG signal of shape (n_leads, n_samples)
            rotation_angle (float): Rotation angle in degrees (-15 to +15 recommended)
            
        Returns:
            np.ndarray: Rotated ECG signal
        """
        angle_rad = np.radians(rotation_angle)
        cos_theta = np.cos(angle_rad)
        sin_theta = np.sin(angle_rad)
        
        # Create rotation matrix for vectorcardiogram-like transformation
        # This affects primarily the precordial leads (V1-V6)
        rotation_matrix = np.array([
            [cos_theta, -sin_theta],
            [sin_theta, cos_theta]
        ])
        
        rotated_signal = ecg_signal.copy()
        n_leads, n_samples = ecg_signal.shape
        
        # Apply rotation to pairs of leads (simulating 2D spatial displacement)
        # Typically affects V1-V2, V3-V4, V5-V6 pairs for precordial leads
        if n_leads >= 8:  # Assuming 12-lead ECG (8 independent + 4 derived)
            for i in range(0, min(6, n_leads-2), 2):  # V1-V6 leads
                lead_pair = ecg_signal[i:i+2, :]
                rotated_pair = rotation_matrix @ lead_pair
                rotated_signal[i:i+2, :] = rotated_pair
        
        return rotated_signal
    
    def apply_time_scaling(self, ecg_signal: np.ndarray, scale_factor: float) -> np.ndarray:
        """
        Apply time-domain scaling to simulate different chest geometries.
        
        Args:
            ecg_signal (np.ndarray): ECG signal of shape (n_leads, n_samples)
            scale_factor (float): Scaling factor (0.9-1.1 recommended)
            
        Returns:
            np.ndarray: Time-scaled ECG signal
        """
        n_leads, n_samples = ecg_signal.shape
        scaled_signal = np.zeros_like(ecg_signal)
        
        # Original time axis
        original_time = np.arange(n_samples)
        # Scaled time axis
        scaled_time = np.arange(n_samples) * scale_factor
        
        for lead_idx in range(n_leads):
            # Interpolate to maintain same number of samples
            interp_func = interp1d(scaled_time, ecg_signal[lead_idx, :], 
                                 kind='cubic', bounds_error=False, fill_value='extrapolate')
            scaled_signal[lead_idx, :] = interp_func(original_time)
        
        return scaled_signal
    
    def apply_inter_lead_delays(self, ecg_signal: np.ndarray, 
                               max_delay_ms: float = 50) -> np.ndarray:
        """
        Apply random delays between leads to simulate asynchronous sampling.
        
        Args:
            ecg_signal (np.ndarray): ECG signal of shape (n_leads, n_samples)
            max_delay_ms (float): Maximum delay in milliseconds
            
        Returns:
            np.ndarray: ECG signal with inter-lead delays
        """
        n_leads, n_samples = ecg_signal.shape
        delayed_signal = np.zeros_like(ecg_signal)
        
        # Convert delay from ms to samples
        max_delay_samples = int(max_delay_ms * self.sampling_rate / 1000)
        
        for lead_idx in range(n_leads):
            # Random delay for each lead
            delay_samples = np.random.randint(-max_delay_samples, max_delay_samples + 1)
            
            if delay_samples > 0:
                # Positive delay: shift right, pad with first value
                delayed_signal[lead_idx, delay_samples:] = ecg_signal[lead_idx, :-delay_samples]
                delayed_signal[lead_idx, :delay_samples] = ecg_signal[lead_idx, 0]
            elif delay_samples < 0:
                # Negative delay: shift left, pad with last value
                delayed_signal[lead_idx, :delay_samples] = ecg_signal[lead_idx, -delay_samples:]
                delayed_signal[lead_idx, delay_samples:] = ecg_signal[lead_idx, -1]
            else:
                # No delay
                delayed_signal[lead_idx, :] = ecg_signal[lead_idx, :]
        
        return delayed_signal
    
    def apply_amplitude_scaling(self, ecg_signal: np.ndarray, 
                              scale_range: Tuple[float, float] = (0.8, 1.2)) -> np.ndarray:
        """
        Apply per-lead amplitude scaling to simulate varying contact quality.
        
        Args:
            ecg_signal (np.ndarray): ECG signal of shape (n_leads, n_samples)
            scale_range (tuple): Min and max scaling factors
            
        Returns:
            np.ndarray: Amplitude-scaled ECG signal
        """
        n_leads, n_samples = ecg_signal.shape
        scaled_signal = np.zeros_like(ecg_signal)
        
        for lead_idx in range(n_leads):
            # Random scaling factor for each lead
            scale_factor = np.random.uniform(scale_range[0], scale_range[1])
            scaled_signal[lead_idx, :] = ecg_signal[lead_idx, :] * scale_factor
        
        return scaled_signal
    
    def apply_combined_spatial_transforms(self, ecg_signal: np.ndarray,
                                        rotation_range: Tuple[float, float] = (-10, 10),
                                        time_scale_range: Tuple[float, float] = (0.95, 1.05),
                                        max_delay_ms: float = 30,
                                        amplitude_range: Tuple[float, float] = (0.85, 1.15),
                                        transform_probability: float = 0.8) -> np.ndarray:
        """
        Apply combined spatial transformations with specified probabilities.
        
        Args:
            ecg_signal (np.ndarray): ECG signal of shape (n_leads, n_samples)
            rotation_range (tuple): Range of rotation angles in degrees
            time_scale_range (tuple): Range of time scaling factors
            max_delay_ms (float): Maximum inter-lead delay in milliseconds
            amplitude_range (tuple): Range of amplitude scaling factors
            transform_probability (float): Probability of applying each transform
            
        Returns:
            np.ndarray: Transformed ECG signal
        """
        transformed_signal = ecg_signal.copy()
        
        # Apply rotation
        if np.random.random() < transform_probability:
            rotation_angle = np.random.uniform(rotation_range[0], rotation_range[1])
            transformed_signal = self.apply_rotation(transformed_signal, rotation_angle)
        
        # Apply time scaling
        if np.random.random() < transform_probability:
            scale_factor = np.random.uniform(time_scale_range[0], time_scale_range[1])
            transformed_signal = self.apply_time_scaling(transformed_signal, scale_factor)
        
        # Apply inter-lead delays
        if np.random.random() < transform_probability:
            transformed_signal = self.apply_inter_lead_delays(transformed_signal, max_delay_ms)
        
        # Apply amplitude scaling
        if np.random.random() < transform_probability:
            transformed_signal = self.apply_amplitude_scaling(transformed_signal, amplitude_range)
        
        return transformed_signal


def create_sample_ecg(n_leads: int = 12, n_samples: int = 5000, 
                     sampling_rate: int = 500) -> np.ndarray:
    """
    Create a synthetic ECG signal for demonstration purposes.
    
    Args:
        n_leads (int): Number of ECG leads
        n_samples (int): Number of samples
        sampling_rate (int): Sampling rate in Hz
        
    Returns:
        np.ndarray: Synthetic ECG signal
    """
    t = np.arange(n_samples) / sampling_rate
    ecg_signal = np.zeros((n_leads, n_samples))
    
    # Create a simple synthetic ECG with P, QRS, T waves
    heart_rate = 70  # BPM
    period = 60 / heart_rate  # seconds
    
    for lead_idx in range(n_leads):
        # Different amplitude and phase for each lead
        amplitude = 0.5 + 0.3 * np.random.random()
        phase_shift = 2 * np.pi * np.random.random()
        
        # P wave (low frequency)
        p_wave = 0.1 * amplitude * np.sin(2 * np.pi * t / period + phase_shift)
        
        # QRS complex (higher frequency)
        qrs_wave = amplitude * np.sin(2 * np.pi * t * 10 / period + phase_shift) * \
                   np.exp(-((t % period - 0.1) / 0.02) ** 2)
        
        # T wave (medium frequency)
        t_wave = 0.3 * amplitude * np.sin(2 * np.pi * t / period + phase_shift + np.pi)
        
        # Add some noise
        noise = 0.02 * np.random.randn(n_samples)
        
        ecg_signal[lead_idx, :] = p_wave + qrs_wave + t_wave + noise
    
    return ecg_signal


# Example usage and demonstration
if __name__ == "__main__":
    # Create sample ECG data
    sampling_rate = 500  # Hz
    duration = 10  # seconds
    n_samples = sampling_rate * duration
    n_leads = 12
    
    # Generate synthetic ECG
    original_ecg = create_sample_ecg(n_leads, n_samples, sampling_rate)
    
    # Initialize spatial transformations
    spatial_transformer = SpatialTransformations(sampling_rate)
    
    print("Spatial Transformations Demonstration")
    print("=" * 40)
    
    # 1. Rotation transformation
    print("1. Applying rotation transformation...")
    rotation_angle = 5.0  # degrees
    rotated_ecg = spatial_transformer.apply_rotation(original_ecg, rotation_angle)
    print(f"   Rotation angle: {rotation_angle}°")
    print(f"   Original signal shape: {original_ecg.shape}")
    print(f"   Rotated signal shape: {rotated_ecg.shape}")
    
    # 2. Time scaling transformation
    print("\n2. Applying time scaling transformation...")
    scale_factor = 1.05
    scaled_ecg = spatial_transformer.apply_time_scaling(original_ecg, scale_factor)
    print(f"   Scale factor: {scale_factor}")
    print(f"   Time scaling applied to simulate chest geometry variation")
    
    # 3. Inter-lead delays
    print("\n3. Applying inter-lead delays...")
    max_delay = 30  # ms
    delayed_ecg = spatial_transformer.apply_inter_lead_delays(original_ecg, max_delay)
    print(f"   Maximum delay: {max_delay} ms")
    print(f"   Random delays applied to each lead")
    
    # 4. Amplitude scaling
    print("\n4. Applying amplitude scaling...")
    amplitude_range = (0.8, 1.2)
    amplitude_scaled_ecg = spatial_transformer.apply_amplitude_scaling(original_ecg, amplitude_range)
    print(f"   Amplitude range: {amplitude_range}")
    print(f"   Per-lead scaling to simulate contact quality variation")
    
    # 5. Combined transformations
    print("\n5. Applying combined spatial transformations...")
    combined_transformed_ecg = spatial_transformer.apply_combined_spatial_transforms(
        original_ecg,
        rotation_range=(-8, 8),
        time_scale_range=(0.95, 1.05),
        max_delay_ms=25,
        amplitude_range=(0.85, 1.15),
        transform_probability=0.7
    )
    print("   Combined transformations applied with 70% probability each")
    
    # Calculate some statistics
    original_std = np.std(original_ecg)
    transformed_std = np.std(combined_transformed_ecg)
    print(f"\n6. Statistics:")
    print(f"   Original signal std: {original_std:.4f}")
    print(f"   Transformed signal std: {transformed_std:.4f}")
    print(f"   Relative change: {(transformed_std/original_std - 1)*100:.2f}%")
    
    # Demonstrate batch processing
    print("\n7. Batch processing example:")
    batch_size = 5
    batch_ecg = np.stack([create_sample_ecg(n_leads, n_samples, sampling_rate) 
                          for _ in range(batch_size)])
    print(f"   Created batch of {batch_size} ECG signals: {batch_ecg.shape}")
    
    # Apply transformations to each sample in batch
    transformed_batch = []
    for i in range(batch_size):
        transformed = spatial_transformer.apply_combined_spatial_transforms(batch_ecg[i])
        transformed_batch.append(transformed)
    
    transformed_batch = np.stack(transformed_batch)
    print(f"   Transformed batch shape: {transformed_batch.shape}")


"""
EXPLANATION OF SPATIAL TRANSFORMATIONS:

This module implements spatial transformations to simulate electrode displacement
in wearable ECG devices compared to hospital-grade 12-lead ECG systems.

KEY CONCEPTS:

1. ROTATION TRANSFORMATION:
   - Simulates electrode displacement by applying 2D rotation to lead pairs
   - Primarily affects precordial leads (V1-V6) which are most sensitive to position
   - Uses rotation matrices to transform the spatial orientation of the electrical vectors
   - Recommended range: ±5-15 degrees to maintain physiological validity

2. TIME-DOMAIN SCALING:
   - Simulates different chest geometries and electrode spacing
   - Uses cubic interpolation to stretch/compress the temporal characteristics
   - Affects all leads uniformly to maintain temporal relationships
   - Recommended range: 0.9-1.1 (±10%) to avoid distorting cardiac physiology

3. INTER-LEAD DELAYS:
   - Simulates asynchronous sampling from displaced electrodes
   - Applies random delays to each lead independently
   - Uses padding to maintain signal length
   - Recommended max delay: 10-50ms (typical for wearable device synchronization issues)

4. AMPLITUDE SCALING:
   - Simulates varying contact quality between electrodes and skin
   - Applies per-lead scaling factors independently
   - Models impedance variations due to contact pressure, moisture, movement
   - Recommended range: 0.8-1.2 (±20%) to simulate realistic contact variations

USAGE SCENARIOS:
- Domain adaptation from hospital ECG to wearable ECG
- Data augmentation for training robust ECG classification models
- Simulation of real-world electrode placement variations
- Testing model robustness to spatial distortions

The transformations are designed to be physiologically plausible while providing
sufficient variability to improve model generalization to wearable devices.
"""
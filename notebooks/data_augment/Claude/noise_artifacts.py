import numpy as np
import torch
from scipy.signal import butter, filtfilt, welch, hilbert
from scipy.interpolate import interp1d
from typing import Tuple, List, Optional, Dict
import matplotlib.pyplot as plt

class NoiseAndArtifactGenerator:
    """
    Generates realistic noise and artifacts for ECG signals to simulate
    wearable device conditions including movement, contact variations,
    and environmental interference.
    """
    
    def __init__(self, sampling_rate: int = 500):
        """
        Initialize noise and artifact generator.
        
        Args:
            sampling_rate (int): ECG sampling rate in Hz
        """
        self.sampling_rate = sampling_rate
        self.nyquist_freq = sampling_rate / 2
    
    def generate_baseline_wander(self, n_samples: int, 
                               amplitude_range: Tuple[float, float] = (0.1, 0.5),
                               frequency_range: Tuple[float, float] = (0.05, 2.0)) -> np.ndarray:
        """
        Generate baseline wander due to respiration and body movement.
        
        Args:
            n_samples (int): Number of samples
            amplitude_range (tuple): Range of wander amplitude (mV)
            frequency_range (tuple): Range of wander frequency (Hz)
            
        Returns:
            np.ndarray: Baseline wander signal
        """
        t = np.arange(n_samples) / self.sampling_rate
        wander = np.zeros(n_samples)
        
        # Respiratory component (main component)
        resp_freq = np.random.uniform(0.2, 0.5)  # 12-30 breaths per minute
        resp_amplitude = np.random.uniform(amplitude_range[0], amplitude_range[1])
        wander += resp_amplitude * np.sin(2 * np.pi * resp_freq * t + np.random.uniform(0, 2*np.pi))
        
        # Movement component (lower frequency)
        movement_freq = np.random.uniform(frequency_range[0], 0.2)
        movement_amplitude = np.random.uniform(amplitude_range[0]/2, amplitude_range[1]/2)
        wander += movement_amplitude * np.sin(2 * np.pi * movement_freq * t + np.random.uniform(0, 2*np.pi))
        
        # Add some harmonics for realism
        harmonic_freq = resp_freq * 2
        harmonic_amplitude = resp_amplitude * 0.3
        wander += harmonic_amplitude * np.sin(2 * np.pi * harmonic_freq * t + np.random.uniform(0, 2*np.pi))
        
        return wander
    
    def generate_muscle_artifacts(self, n_samples: int,
                                activity_level: str = 'moderate',
                                duration_ratio: float = 0.3) -> np.ndarray:
        """
        Generate muscle artifacts (EMG) due to body movement.
        
        Args:
            n_samples (int): Number of samples
            activity_level (str): Activity level ('low', 'moderate', 'high')
            duration_ratio (float): Fraction of signal with muscle artifacts
            
        Returns:
            np.ndarray: Muscle artifact signal
        """
        # EMG amplitude ranges based on activity level
        amplitude_ranges = {
            'low': (0.02, 0.08),
            'moderate': (0.05, 0.15),
            'high': (0.1, 0.3)
        }
        
        amplitude_range = amplitude_ranges.get(activity_level, amplitude_ranges['moderate'])
        
        # Create muscle artifact bursts
        muscle_artifact = np.zeros(n_samples)
        
        # Determine artifact regions
        n_artifact_samples = int(n_samples * duration_ratio)
        artifact_regions = []
        
        # Create random artifact bursts
        n_bursts = np.random.randint(3, 8)  # 3-8 bursts
        burst_samples = n_artifact_samples // n_bursts
        
        for i in range(n_bursts):
            # Random start position
            start_pos = np.random.randint(0, n_samples - burst_samples)
            # Random burst duration
            burst_duration = np.random.randint(burst_samples//2, burst_samples)
            end_pos = min(start_pos + burst_duration, n_samples)
            
            artifact_regions.append((start_pos, end_pos))
        
        # Generate EMG-like signal in artifact regions
        for start, end in artifact_regions:
            duration = end - start
            t_burst = np.arange(duration) / self.sampling_rate
            
            # EMG characteristics: 20-200 Hz, with most energy in 50-150 Hz
            emg_signal = np.zeros(duration)
            
            # Multiple frequency components
            for freq in np.random.uniform(20, 200, 10):
                amplitude = np.random.uniform(amplitude_range[0], amplitude_range[1])
                phase = np.random.uniform(0, 2*np.pi)
                emg_signal += amplitude * np.sin(2 * np.pi * freq * t_burst + phase)
            
            # Apply envelope (muscle contraction profile)
            envelope = np.exp(-0.5 * ((t_burst - duration/(2*self.sampling_rate)) / (duration/(4*self.sampling_rate)))**2)
            emg_signal *= envelope
            
            # Add to main signal
            muscle_artifact[start:end] += emg_signal
        
        return muscle_artifact
    
    def generate_powerline_interference(self, n_samples: int,
                                      frequency: float = 60.0,
                                      amplitude_range: Tuple[float, float] = (0.01, 0.1),
                                      harmonic_count: int = 3) -> np.ndarray:
        """
        Generate powerline interference (50/60 Hz and harmonics).
        
        Args:
            n_samples (int): Number of samples
            frequency (float): Powerline frequency (50 or 60 Hz)
            amplitude_range (tuple): Range of interference amplitude
            harmonic_count (int): Number of harmonics to include
            
        Returns:
            np.ndarray: Powerline interference signal
        """
        t = np.arange(n_samples) / self.sampling_rate
        interference = np.zeros(n_samples)
        
        # Main frequency component
        main_amplitude = np.random.uniform(amplitude_range[0], amplitude_range[1])
        main_phase = np.random.uniform(0, 2*np.pi)
        interference += main_amplitude * np.sin(2 * np.pi * frequency * t + main_phase)
        
        # Add harmonics
        for harmonic in range(2, harmonic_count + 2):
            harmonic_freq = frequency * harmonic
            if harmonic_freq < self.nyquist_freq:
                harmonic_amplitude = main_amplitude / harmonic  # Decreasing amplitude
                harmonic_phase = np.random.uniform(0, 2*np.pi)
                interference += harmonic_amplitude * np.sin(2 * np.pi * harmonic_freq * t + harmonic_phase)
        
        # Add some amplitude modulation (realistic power grid fluctuations)
        modulation_freq = np.random.uniform(0.1, 2.0)
        modulation_depth = 0.2
        modulation = 1 + modulation_depth * np.sin(2 * np.pi * modulation_freq * t)
        interference *= modulation
        
        return interference
    
    def generate_contact_variations(self, n_samples: int,
                                  base_impedance: float = 1.0,
                                  variation_frequency: float = 0.5,
                                  dropout_probability: float = 0.02) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate contact quality variations and dropout events.
        
        Args:
            n_samples (int): Number of samples
            base_impedance (float): Base impedance level
            variation_frequency (float): Frequency of impedance variations (Hz)
            dropout_probability (float): Probability of dropout events per sample
            
        Returns:
            tuple: (impedance_variations, dropout_mask)
        """
        t = np.arange(n_samples) / self.sampling_rate
        
        # Impedance variations (slow changes in contact quality)
        impedance_variations = base_impedance * (
            1.0 + 0.3 * np.sin(2 * np.pi * variation_frequency * t + np.random.uniform(0, 2*np.pi)) +
            0.1 * np.random.randn(n_samples)  # Random variations
        )
        
        # Ensure positive impedance
        impedance_variations = np.maximum(impedance_variations, 0.1)
        
        # Generate dropout events (brief signal loss)
        dropout_mask = np.ones(n_samples)
        dropout_events = np.random.random(n_samples) < dropout_probability
        
        # Extend dropout events to create realistic brief interruptions
        for i in range(n_samples):
            if dropout_events[i]:
                # Create dropout of 10-100 ms duration
                dropout_duration = np.random.randint(
                    int(0.01 * self.sampling_rate),  # 10 ms
                    int(0.1 * self.sampling_rate)    # 100 ms
                )
                end_idx = min(i + dropout_duration, n_samples)
                dropout_mask[i:end_idx] = 0
        
        return impedance_variations, dropout_mask
    
    def generate_motion_artifacts(self, n_samples: int,
                                motion_type: str = 'walking',
                                intensity: float = 1.0) -> np.ndarray:
        """
        Generate motion-specific artifacts.
        
        Args:
            n_samples (int): Number of samples
            motion_type (str): Type of motion ('walking', 'running', 'arm_movement', 'sitting')
            intensity (float): Motion intensity multiplier
            
        Returns:
            np.ndarray: Motion artifact signal
        """
        t = np.arange(n_samples) / self.sampling_rate
        motion_artifact = np.zeros(n_samples)
        
        if motion_type == 'walking':
            # Walking: ~1-2 Hz fundamental with harmonics
            step_freq = np.random.uniform(1.0, 2.0)  # steps per second
            
            # Main stepping component
            amplitude = 0.1 * intensity
            motion_artifact += amplitude * np.sin(2 * np.pi * step_freq * t)
            
            # Harmonics
            motion_artifact += 0.05 * intensity * np.sin(2 * np.pi * step_freq * 2 * t + np.pi/4)
            motion_artifact += 0.02 * intensity * np.sin(2 * np.pi * step_freq * 3 * t + np.pi/2)
            
            # Add some irregularity
            irregularity = 0.02 * intensity * np.random.randn(n_samples)
            motion_artifact += irregularity
            
        elif motion_type == 'running':
            # Running: higher frequency and amplitude
            step_freq = np.random.uniform(2.5, 4.0)
            amplitude = 0.2 * intensity
            
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
            motion_artifact += amplitude * np.sin(2 * np.pi * step_freq * t)
            motion_artifact += 0.1 * intensity * np.sin(2 * np.pi * step_freq * 2 * t + np.pi/3)
            motion_artifact += 0.05 * intensity * np.sin(2 * np.pi * step_freq * 3 * t + np.pi/6)
            
            # More pronounced irregularity for running
            irregularity = 0.05 * intensity * np.random.randn(n_samples)
            motion_artifact += irregularity
            
        elif motion_type == 'arm_movement':
            # Arm movement: lower frequency, larger amplitude variations
            movement_freq = np.random.uniform(0.5, 1.5)
            amplitude = 0.15 * intensity
            
            # Sinusoidal movement with envelope
            envelope_freq = np.random.uniform(0.1, 0.3)
            envelope = 1 + 0.5 * np.sin(2 * np.pi * envelope_freq * t)
            motion_artifact += amplitude * envelope * np.sin(2 * np.pi * movement_freq * t)
            
        elif motion_type == 'sitting':
            # Sitting: minimal motion, mostly micro-movements
            amplitude = 0.02 * intensity
            micro_freq = np.random.uniform(0.1, 0.5)
            motion_artifact += amplitude * np.sin(2 * np.pi * micro_freq * t)
            
            # Add some random micro-movements
            micro_movements = 0.01 * intensity * np.random.randn(n_samples)
            motion_artifact += micro_movements
        
        # Apply low-pass filtering to make motion artifacts more realistic
        if np.any(motion_artifact):
            b, a = butter(3, 10 / self.nyquist_freq, btype='low')
            motion_artifact = filtfilt(b, a, motion_artifact)
        
        return motion_artifact
    
    def generate_electrode_pop_artifacts(self, n_samples: int,
                                       pop_rate: float = 0.1) -> np.ndarray:
        """
        Generate electrode pop/click artifacts due to sudden contact changes.
        
        Args:
            n_samples (int): Number of samples
            pop_rate (float): Average pops per second
            
        Returns:
            np.ndarray: Electrode pop artifacts
        """
        pop_artifact = np.zeros(n_samples)
        
        # Calculate expected number of pops
        duration = n_samples / self.sampling_rate
        expected_pops = int(pop_rate * duration)
        
        # Generate random pop locations
        pop_locations = np.random.randint(0, n_samples, expected_pops)
        
        for pop_loc in pop_locations:
            # Pop characteristics
            amplitude = np.random.uniform(0.1, 0.5)
            duration_samples = np.random.randint(1, 10)  # 1-10 samples (2-20ms at 500Hz)
            
            # Create exponential decay pop
            end_loc = min(pop_loc + duration_samples, n_samples)
            pop_duration = end_loc - pop_loc
            
            if pop_duration > 0:
                decay = np.exp(-np.arange(pop_duration) / (duration_samples / 3))
                pop_signal = amplitude * decay * np.random.choice([-1, 1])  # Random polarity
                pop_artifact[pop_loc:end_loc] += pop_signal
        
        return pop_artifact
    
    def generate_thermal_noise(self, n_samples: int,
                             noise_density: float = 0.01) -> np.ndarray:
        """
        Generate thermal (white) noise from electronics.
        
        Args:
            n_samples (int): Number of samples
            noise_density (float): Noise density (mV)
            
        Returns:
            np.ndarray: Thermal noise signal
        """
        return noise_density * np.random.randn(n_samples)
    
    def generate_quantization_noise(self, signal: np.ndarray,
                                  bit_depth: int = 12) -> np.ndarray:
        """
        Add quantization noise based on ADC bit depth.
        
        Args:
            signal (np.ndarray): Input signal
            bit_depth (int): ADC bit depth
            
        Returns:
            np.ndarray: Signal with quantization noise
        """
        # Calculate quantization step
        signal_range = np.max(signal) - np.min(signal)
        q_step = signal_range / (2**bit_depth)
        
        # Quantize signal
        quantized = np.round(signal / q_step) * q_step
        
        # Add uniform quantization noise
        noise = np.random.uniform(-q_step/2, q_step/2, signal.shape)
        
        return quantized + noise
    
    def apply_signal_dependent_noise(self, signal: np.ndarray,
                                   noise_factor: float = 0.05) -> np.ndarray:
        """
        Apply signal-dependent noise (multiplicative noise).
        
        Args:
            signal (np.ndarray): Input signal
            noise_factor (float): Noise factor (fraction of signal amplitude)
            
        Returns:
            np.ndarray: Signal with multiplicative noise
        """
        # Calculate local signal amplitude
        signal_envelope = np.abs(hilbert(signal))
        
        # Generate noise proportional to signal amplitude
        noise = noise_factor * signal_envelope * np.random.randn(len(signal))
        
        return signal + noise
    
    def apply_combined_noise_and_artifacts(self, ecg_signal: np.ndarray,
                                         noise_config: Optional[Dict] = None) -> np.ndarray:
        """
        Apply combined noise and artifacts to ECG signal.
        
        Args:
            ecg_signal (np.ndarray): Clean ECG signal of shape (n_leads, n_samples)
            noise_config (dict): Configuration for noise parameters
            
        Returns:
            np.ndarray: ECG signal with noise and artifacts
        """
        if noise_config is None:
            noise_config = {
                'baseline_wander': {'enable': True, 'amplitude_range': (0.1, 0.3)},
                'muscle_artifacts': {'enable': True, 'activity_level': 'moderate', 'duration_ratio': 0.2},
                'powerline_interference': {'enable': True, 'frequency': 60.0, 'amplitude_range': (0.02, 0.08)},
                'motion_artifacts': {'enable': True, 'motion_type': 'walking', 'intensity': 0.8},
                'contact_variations': {'enable': True, 'dropout_probability': 0.01},
                'electrode_pops': {'enable': True, 'pop_rate': 0.05},
                'thermal_noise': {'enable': True, 'noise_density': 0.015},
                'quantization_noise': {'enable': True, 'bit_depth': 12},
                'signal_dependent_noise': {'enable': True, 'noise_factor': 0.03}
            }
        
        n_leads, n_samples = ecg_signal.shape
        noisy_ecg = ecg_signal.copy()
        
        for lead_idx in range(n_leads):
            lead_signal = noisy_ecg[lead_idx, :]
            
            # 1. Baseline wander
            if noise_config['baseline_wander']['enable']:
                baseline_wander = self.generate_baseline_wander(
                    n_samples, 
                    amplitude_range=noise_config['baseline_wander']['amplitude_range']
                )
                lead_signal += baseline_wander
            
            # 2. Muscle artifacts (apply to random subset of leads)
            if noise_config['muscle_artifacts']['enable'] and np.random.random() < 0.7:
                muscle_artifacts = self.generate_muscle_artifacts(
                    n_samples,
                    activity_level=noise_config['muscle_artifacts']['activity_level'],
                    duration_ratio=noise_config['muscle_artifacts']['duration_ratio']
                )
                lead_signal += muscle_artifacts
            
            # 3. Powerline interference
            if noise_config['powerline_interference']['enable']:
                powerline_noise = self.generate_powerline_interference(
                    n_samples,
                    frequency=noise_config['powerline_interference']['frequency'],
                    amplitude_range=noise_config['powerline_interference']['amplitude_range']
                )
                lead_signal += powerline_noise
            
            # 4. Motion artifacts
            if noise_config['motion_artifacts']['enable']:
                motion_artifacts = self.generate_motion_artifacts(
                    n_samples,
                    motion_type=noise_config['motion_artifacts']['motion_type'],
                    intensity=noise_config['motion_artifacts']['intensity']
                )
                lead_signal += motion_artifacts
            
            # 5. Contact variations and dropouts
            if noise_config['contact_variations']['enable']:
                impedance_variations, dropout_mask = self.generate_contact_variations(
                    n_samples,
                    dropout_probability=noise_config['contact_variations']['dropout_probability']
                )
                # Apply impedance variations as multiplicative factor
                lead_signal *= (1.0 / impedance_variations)
                # Apply dropouts
                lead_signal *= dropout_mask
            
            # 6. Electrode pop artifacts
            if noise_config['electrode_pops']['enable']:
                pop_artifacts = self.generate_electrode_pop_artifacts(
                    n_samples,
                    pop_rate=noise_config['electrode_pops']['pop_rate']
                )
                lead_signal += pop_artifacts
            
            # 7. Thermal noise
            if noise_config['thermal_noise']['enable']:
                thermal_noise = self.generate_thermal_noise(
                    n_samples,
                    noise_density=noise_config['thermal_noise']['noise_density']
                )
                lead_signal += thermal_noise
            
            # 8. Signal-dependent noise
            if noise_config['signal_dependent_noise']['enable']:
                lead_signal = self.apply_signal_dependent_noise(
                    lead_signal,
                    noise_factor=noise_config['signal_dependent_noise']['noise_factor']
                )
            
            # 9. Quantization noise (applied last)
            if noise_config['quantization_noise']['enable']:
                lead_signal = self.generate_quantization_noise(
                    lead_signal,
                    bit_depth=noise_config['quantization_noise']['bit_depth']
                )
            
            noisy_ecg[lead_idx, :] = lead_signal
        
        return noisy_ecg
    
    def create_activity_specific_noise_profile(self, activity: str) -> Dict:
        """
        Create noise configuration profiles for specific activities.
        
        Args:
            activity (str): Activity type ('resting', 'walking', 'running', 'daily_activities')
            
        Returns:
            Dict: Noise configuration for the activity
        """
        profiles = {
            'resting': {
                'baseline_wander': {'enable': True, 'amplitude_range': (0.05, 0.15)},
                'muscle_artifacts': {'enable': True, 'activity_level': 'low', 'duration_ratio': 0.1},
                'powerline_interference': {'enable': True, 'frequency': 60.0, 'amplitude_range': (0.01, 0.05)},
                'motion_artifacts': {'enable': True, 'motion_type': 'sitting', 'intensity': 0.3},
                'contact_variations': {'enable': True, 'dropout_probability': 0.005},
                'electrode_pops': {'enable': True, 'pop_rate': 0.02},
                'thermal_noise': {'enable': True, 'noise_density': 0.01},
                'quantization_noise': {'enable': True, 'bit_depth': 12},
                'signal_dependent_noise': {'enable': True, 'noise_factor': 0.02}
            },
            'walking': {
                'baseline_wander': {'enable': True, 'amplitude_range': (0.15, 0.4)},
                'muscle_artifacts': {'enable': True, 'activity_level': 'moderate', 'duration_ratio': 0.3},
                'powerline_interference': {'enable': True, 'frequency': 60.0, 'amplitude_range': (0.02, 0.08)},
                'motion_artifacts': {'enable': True, 'motion_type': 'walking', 'intensity': 1.0},
                'contact_variations': {'enable': True, 'dropout_probability': 0.015},
                'electrode_pops': {'enable': True, 'pop_rate': 0.08},
                'thermal_noise': {'enable': True, 'noise_density': 0.015},
                'quantization_noise': {'enable': True, 'bit_depth': 12},
                'signal_dependent_noise': {'enable': True, 'noise_factor': 0.04}
            },
            'running': {
                'baseline_wander': {'enable': True, 'amplitude_range': (0.3, 0.8)},
                'muscle_artifacts': {'enable': True, 'activity_level': 'high', 'duration_ratio': 0.5},
                'powerline_interference': {'enable': True, 'frequency': 60.0, 'amplitude_range': (0.03, 0.12)},
                'motion_artifacts': {'enable': True, 'motion_type': 'running', 'intensity': 1.5},
                'contact_variations': {'enable': True, 'dropout_probability': 0.025},
                'electrode_pops': {'enable': True, 'pop_rate': 0.15},
                'thermal_noise': {'enable': True, 'noise_density': 0.02},
                'quantization_noise': {'enable': True, 'bit_depth': 12},
                'signal_dependent_noise': {'enable': True, 'noise_factor': 0.06}
            },
            'daily_activities': {
                'baseline_wander': {'enable': True, 'amplitude_range': (0.1, 0.3)},
                'muscle_artifacts': {'enable': True, 'activity_level': 'moderate', 'duration_ratio': 0.25},
                'powerline_interference': {'enable': True, 'frequency': 60.0, 'amplitude_range': (0.02, 0.1)},
                'motion_artifacts': {'enable': True, 'motion_type': 'arm_movement', 'intensity': 0.8},
                'contact_variations': {'enable': True, 'dropout_probability': 0.01},
                'electrode_pops': {'enable': True, 'pop_rate': 0.06},
                'thermal_noise': {'enable': True, 'noise_density': 0.015},
                'quantization_noise': {'enable': True, 'bit_depth': 12},
                'signal_dependent_noise': {'enable': True, 'noise_factor': 0.035}
            }
        }
        
        return profiles.get(activity, profiles['walking'])


def create_sample_clean_ecg(n_leads: int = 12, n_samples: int = 5000, 
                           sampling_rate: int = 500) -> np.ndarray:
    """
    Create a clean synthetic ECG signal for noise demonstration.
    
    Args:
        n_leads (int): Number of ECG leads
        n_samples (int): Number of samples
        sampling_rate (int): Sampling rate in Hz
        
    Returns:
        np.ndarray: Clean synthetic ECG signal
    """
    t = np.arange(n_samples) / sampling_rate
    ecg_signal = np.zeros((n_leads, n_samples))
    
    # Heart rate parameters
    heart_rate = 72  # BPM
    rr_interval = 60 / heart_rate  # seconds
    
    # Lead-specific amplitudes (simplified 12-lead characteristics)
    lead_amplitudes = [0.8, 1.2, 0.6, -0.4, 0.5, 1.0,  # I, II, III, aVR, aVL, aVF
                      -0.3, 0.4, 0.8, 1.5, 1.2, 1.0]    # V1, V2, V3, V4, V5, V6
    
    for lead_idx in range(min(n_leads, len(lead_amplitudes))):
        amplitude = lead_amplitudes[lead_idx]
        
        # Generate cardiac cycles
        signal = np.zeros(n_samples)
        n_beats = int(len(t) / (rr_interval * sampling_rate)) + 1
        
        for beat in range(n_beats):
            beat_start_time = beat * rr_interval
            beat_start_idx = int(beat_start_time * sampling_rate)
            
            if beat_start_idx >= n_samples:
                break
            
            # QRS complex (dominant feature)
            qrs_start = beat_start_idx + int(0.12 * sampling_rate)  # 120ms PR interval
            qrs_duration = int(0.08 * sampling_rate)  # 80ms QRS duration
            qrs_end = min(qrs_start + qrs_duration, n_samples)
            
            if qrs_start < n_samples:
                qrs_indices = np.arange(qrs_start, qrs_end)
                qrs_time = (qrs_indices - qrs_start) / sampling_rate
                qrs_normalized_time = qrs_time / (qrs_duration / sampling_rate)
                
                # QRS shape (simplified)
                qrs_shape = amplitude * np.sin(np.pi * qrs_normalized_time * 3) * \
                           np.exp(-((qrs_normalized_time - 0.5) / 0.3)**2)
                signal[qrs_indices] += qrs_shape
            
            # T wave
            t_start = beat_start_idx + int(0.3 * sampling_rate)  # 300ms after beat start
            t_duration = int(0.15 * sampling_rate)  # 150ms T wave duration
            t_end = min(t_start + t_duration, n_samples)
            
            if t_start < n_samples:
                t_indices = np.arange(t_start, t_end)
                t_time = (t_indices - t_start) / sampling_rate
                t_normalized_time = t_time / (t_duration / sampling_rate)
                
                # T wave shape
                t_shape = 0.3 * amplitude * np.exp(-((t_normalized_time - 0.5) / 0.4)**2)
                signal[t_indices] += t_shape
        
        ecg_signal[lead_idx, :] = signal
    
    return ecg_signal


# Example usage and demonstration
if __name__ == "__main__":
    # Create sample clean ECG data
    sampling_rate = 500  # Hz
    duration = 10  # seconds
    n_samples = sampling_rate * duration
    n_leads = 12
    
    # Generate clean synthetic ECG
    clean_ecg = create_sample_clean_ecg(n_leads, n_samples, sampling_rate)
    
    # Initialize noise and artifact generator
    noise_generator = NoiseAndArtifactGenerator(sampling_rate)
    
    print("Noise and Artifact Generation Demonstration")
    print("=" * 50)
    
    # 1. Individual noise components
    print("1. Generating individual noise components...")
    
    # Baseline wander
    baseline_wander = noise_generator.generate_baseline_wander(n_samples)
    print(f"   Baseline wander: amplitude range = {np.min(baseline_wander):.3f} to {np.max(baseline_wander):.3f} mV")
    
    # Muscle artifacts
    muscle_artifacts = noise_generator.generate_muscle_artifacts(n_samples, activity_level='moderate')
    muscle_power = np.mean(muscle_artifacts**2)
    print(f"   Muscle artifacts: RMS power = {muscle_power:.6f}")
    
    # Powerline interference
    powerline_noise = noise_generator.generate_powerline_interference(n_samples, frequency=60.0)
    print(f"   Powerline interference: peak amplitude = {np.max(np.abs(powerline_noise)):.3f} mV")
    
    # Motion artifacts for different activities
    motion_types = ['walking', 'running', 'sitting', 'arm_movement']
    for motion_type in motion_types:
        motion_artifact = noise_generator.generate_motion_artifacts(n_samples, motion_type=motion_type)
        motion_rms = np.sqrt(np.mean(motion_artifact**2))
        print(f"   {motion_type.capitalize()} motion: RMS = {motion_rms:.4f} mV")
    
    # Contact variations
    impedance_vars, dropout_mask = noise_generator.generate_contact_variations(n_samples)
    dropout_percentage = (1 - np.mean(dropout_mask)) * 100
    print(f"   Contact variations: {dropout_percentage:.2f}% signal dropout")
    
    # Electrode pops
    pop_artifacts = noise_generator.generate_electrode_pop_artifacts(n_samples, pop_rate=0.1)
    n_pops = np.sum(np.abs(pop_artifacts) > 0.01)
    print(f"   Electrode pops: {n_pops} pop events detected")
    
    # Thermal noise
    thermal_noise = noise_generator.generate_thermal_noise(n_samples)
    thermal_std = np.std(thermal_noise)
    print(f"   Thermal noise: standard deviation = {thermal_std:.4f} mV")
    
    print("\n2. Applying combined noise to ECG signals...")
    
    # Test different activity profiles
    activities = ['resting', 'walking', 'running', 'daily_activities']
    
    for activity in activities:
        noise_config = noise_generator.create_activity_specific_noise_profile(activity)
        noisy_ecg = noise_generator.apply_combined_noise_and_artifacts(clean_ecg, noise_config)
        
        # Calculate SNR
        signal_power = np.mean(clean_ecg**2)
        noise_power = np.mean((noisy_ecg - clean_ecg)**2)
        snr_db = 10 * np.log10(signal_power / noise_power) if noise_power > 0 else float('inf')
        
        print(f"   {activity.capitalize()}: SNR = {snr_db:.1f} dB")
    
    print("\n3. Lead-specific noise analysis...")
    
    # Apply noise to individual leads and analyze
    test_config = noise_generator.create_activity_specific_noise_profile('walking')
    noisy_ecg_test = noise_generator.apply_combined_noise_and_artifacts(clean_ecg, test_config)
    
    lead_names = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
    
    for lead_idx in range(min(n_leads, len(lead_names))):
        clean_lead = clean_ecg[lead_idx, :]
        noisy_lead = noisy_ecg_test[lead_idx, :]
        
        correlation = np.corrcoef(clean_lead, noisy_lead)[0, 1]
        rmse = np.sqrt(np.mean((clean_lead - noisy_lead)**2))
        
        print(f"   Lead {lead_names[lead_idx]}: correlation = {correlation:.3f}, RMSE = {rmse:.4f}")
    
    print("\n4. Quantization noise demonstration...")
    
    # Test different bit depths
    bit_depths = [8, 10, 12, 16]
    test_signal = clean_ecg[1, :]  # Use Lead II
    
    for bit_depth in bit_depths:
        quantized_signal = noise_generator.generate_quantization_noise(test_signal, bit_depth)
        quantization_error = np.std(test_signal - quantized_signal)
        print(f"   {bit_depth}-bit ADC: quantization error std = {quantization_error:.6f}")
    
    print("\n5. Batch processing demonstration...")
    
    # Create batch of ECG signals
    batch_size = 4
    batch_ecg = np.stack([create_sample_clean_ecg(n_leads, n_samples, sampling_rate) 
                          for _ in range(batch_size)])
    print(f"   Created batch of {batch_size} clean ECG signals: {batch_ecg.shape}")
    
    # Apply different noise profiles to each sample
    noise_profiles = ['resting', 'walking', 'running', 'daily_activities']
    noisy_batch = []
    
    for i in range(batch_size):
        profile = noise_profiles[i % len(noise_profiles)]
        noise_config = noise_generator.create_activity_specific_noise_profile(profile)
        noisy_sample = noise_generator.apply_combined_noise_and_artifacts(batch_ecg[i], noise_config)
        noisy_batch.append(noisy_sample)
    
    noisy_batch = np.stack(noisy_batch)
    print(f"   Processed noisy batch shape: {noisy_batch.shape}")
    
    # Calculate batch statistics
    clean_batch_power = np.mean([np.mean(batch_ecg[i]**2) for i in range(batch_size)])
    noisy_batch_power = np.mean([np.mean(noisy_batch[i]**2) for i in range(batch_size)])
    print(f"   Average signal power - Clean: {clean_batch_power:.6f}, Noisy: {noisy_batch_power:.6f}")
    
    print("\n6. Custom noise configuration example...")
    
    # Create custom noise configuration
    custom_config = {
        'baseline_wander': {'enable': True, 'amplitude_range': (0.2, 0.5)},
        'muscle_artifacts': {'enable': False},
        'powerline_interference': {'enable': True, 'frequency': 50.0, 'amplitude_range': (0.05, 0.15)},
        'motion_artifacts': {'enable': True, 'motion_type': 'walking', 'intensity': 1.2},
        'contact_variations': {'enable': True, 'dropout_probability': 0.02},
        'electrode_pops': {'enable': False},
        'thermal_noise': {'enable': True, 'noise_density': 0.025},
        'quantization_noise': {'enable': True, 'bit_depth': 10},
        'signal_dependent_noise': {'enable': True, 'noise_factor': 0.05}
    }
    
    custom_noisy_ecg = noise_generator.apply_combined_noise_and_artifacts(clean_ecg, custom_config)
    
    # Analyze custom configuration results
    signal_power = np.mean(clean_ecg**2)
    noise_power = np.mean((custom_noisy_ecg - clean_ecg)**2)
    custom_snr = 10 * np.log10(signal_power / noise_power)
    print(f"   Custom configuration: SNR = {custom_snr:.1f} dB")
    print(f"   Custom configuration applied successfully!")


"""
EXPLANATION OF NOISE AND ARTIFACT GENERATION:

This module generates realistic noise and artifacts that occur in wearable ECG devices,
particularly shirt-based systems, to create training data that bridges the gap between
clean hospital ECG recordings and real-world wearable device conditions.

KEY NOISE COMPONENTS:

1. BASELINE WANDER:
   - Low-frequency drift (0.05-2 Hz) from respiration and body movement
   - Primary component: respiratory frequency (12-30 breaths/min = 0.2-0.5 Hz)
   - Secondary component: body movement (slower, 0.05-0.2 Hz)
   - Includes harmonic components for realism
   - Most significant artifact in wearable devices

2. MUSCLE ARTIFACTS (EMG):
   - High-frequency noise (20-200 Hz) from muscle contractions
   - Activity-dependent: low/moderate/high intensity levels
   - Burst-like pattern with exponential decay envelopes
   - Most energy in 50-150 Hz band (typical EMG characteristics)
   - Duration and frequency depend on physical activity level

3. POWERLINE INTERFERENCE:
   - 50/60 Hz fundamental frequency with harmonics
   - Amplitude modulation from power grid fluctuations
   - Variable amplitude based on environment and electrode contact
   - Includes 2nd and 3rd harmonics (120/180 Hz or 100/150 Hz)

4. MOTION ARTIFACTS:
   - Activity-specific patterns:
     * Walking: 1-2 Hz fundamental with harmonics
     * Running: 2.5-4 Hz with higher amplitude
     * Arm movement: 0.5-1.5 Hz with envelope modulation
     * Sitting: minimal micro-movements (0.1-0.5 Hz)
   - Low-pass filtered for realistic characteristics

5. CONTACT QUALITY VARIATIONS:
   - Slow impedance changes affecting signal amplitude
   - Brief dropout events (10-100 ms) simulating contact loss
   - More frequent in loose-fitting garments
   - Multiplicative effect on signal amplitude

6. ELECTRODE POP ARTIFACTS:
   - Brief, high-amplitude transients from sudden contact changes
   - Exponential decay pattern (1-10 samples duration)
   - Random polarity and occurrence rate
   - Common in fabric-based electrode systems

7. THERMAL NOISE:
   - White Gaussian noise from electronic components
   - Additive noise with configurable density
   - Represents amplifier and ADC noise floor
   - Typically much smaller than other artifact sources

8. QUANTIZATION NOISE:
   - Digital conversion artifacts from ADC bit depth
   - Uniform distribution within quantization step
   - More significant with lower bit depths (8-10 bit)
   - Models limitations of low-power wearable electronics

9. SIGNAL-DEPENDENT NOISE:
   - Multiplicative noise proportional to signal amplitude
   - Uses Hilbert transform for envelope detection
   - Models impedance-dependent noise variations
   - Realistic for contact-based measurement systems

ACTIVITY-SPECIFIC PROFILES:

The module includes predefined noise profiles for different activities:
- RESTING: minimal motion, low muscle activity, good contact
- WALKING: moderate motion artifacts, periodic movement patterns
- RUNNING: high motion artifacts, significant muscle activity
- DAILY_ACTIVITIES: variable motion, arm movement artifacts

USAGE FOR WEARABLE ECG TRAINING:

1. Domain Adaptation: Bridges clean hospital ECG to noisy wearable data
2. Robustness Training: Improves model performance under real conditions
3. Data Augmentation: Increases dataset diversity with realistic variations
4. Evaluation: Tests model performance across different noise conditions

The noise models are based on empirical studies of wearable ECG devices and
maintain physiological plausibility while providing sufficient challenge
for training robust ECG classification models.

TECHNICAL IMPLEMENTATION NOTES:

1. All noise components are generated independently and combined additively
   or multiplicatively as appropriate to their physical nature
2. Frequency domain characteristics match published literature on ECG artifacts
3. Amplitude ranges are calibrated to typical wearable device measurements
4. Temporal patterns reflect realistic human physiology and movement
5. Random parameters ensure dataset diversity while maintaining realism

RECOMMENDED USAGE PATTERNS:

- Use 'resting' profile for baseline model training
- Apply 'walking' profile for general wearable device simulation
- Use 'running' profile for stress testing model robustness
- Combine multiple profiles in training batches for comprehensive coverage
- Adjust noise parameters based on your specific device characteristics

The module supports both single-sample processing and efficient batch processing
for large-scale dataset augmentation workflows."""
            
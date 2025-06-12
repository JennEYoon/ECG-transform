import numpy as np
import torch
from scipy.signal import butter, filtfilt, hilbert
from scipy.interpolate import interp1d
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt

class AnatomicalVariationSimulator:
    """
    Simulates anatomical variations in ECG signals to model how electrode displacement
    in shirt-based systems affects signal morphology compared to standard 12-lead placement.
    """
    
    def __init__(self, sampling_rate: int = 500):
        """
        Initialize anatomical variation simulator.
        
        Args:
            sampling_rate (int): ECG sampling rate in Hz
        """
        self.sampling_rate = sampling_rate
        
        # Define standard 12-lead ECG lead positions and their relationships
        self.lead_positions = {
            'I': {'type': 'limb', 'vector': [1, 0], 'reference_leads': []},
            'II': {'type': 'limb', 'vector': [0.5, -0.866], 'reference_leads': []},
            'III': {'type': 'limb', 'vector': [-0.5, -0.866], 'reference_leads': []},
            'aVR': {'type': 'augmented', 'vector': [-0.5, 0.866], 'reference_leads': ['I', 'II']},
            'aVL': {'type': 'augmented', 'vector': [0.5, 0.866], 'reference_leads': ['I', 'III']},
            'aVF': {'type': 'augmented', 'vector': [0, -1], 'reference_leads': ['II', 'III']},
            'V1': {'type': 'precordial', 'vector': [0.2, -0.8], 'reference_leads': []},
            'V2': {'type': 'precordial', 'vector': [0.4, -0.6], 'reference_leads': []},
            'V3': {'type': 'precordial', 'vector': [0.6, -0.4], 'reference_leads': []},
            'V4': {'type': 'precordial', 'vector': [0.8, -0.2], 'reference_leads': []},
            'V5': {'type': 'precordial', 'vector': [0.9, 0.1], 'reference_leads': []},
            'V6': {'type': 'precordial', 'vector': [1.0, 0.3], 'reference_leads': []}
        }
        
        # Lead sensitivity to displacement (higher = more sensitive)
        self.displacement_sensitivity = {
            'limb': 0.3,      # Limb leads less affected by chest displacement
            'augmented': 0.4,  # Augmented leads moderately affected
            'precordial': 1.0  # Precordial leads most affected by chest displacement
        }
    
    def create_lead_transformation_matrix(self, displacement_pattern: str = 'shirt_generic') -> np.ndarray:
        """
        Create transformation matrix for specific displacement patterns.
        
        Args:
            displacement_pattern (str): Type of displacement pattern
                - 'shirt_generic': Generic shirt-based displacement
                - 'shirt_tight': Tight-fitting shirt
                - 'shirt_loose': Loose-fitting shirt
                - 'custom': User-defined pattern
                
        Returns:
            np.ndarray: Lead transformation matrix (12x12)
        """
        n_leads = 12
        transformation_matrix = np.eye(n_leads)
        
        if displacement_pattern == 'shirt_generic':
            # Generic shirt displacement: precordial leads shifted up/down
            # V1-V2: slight upward displacement
            transformation_matrix[6, 6] = 0.9   # V1 reduced amplitude
            transformation_matrix[6, 7] = 0.1   # V1 gets component from V2
            transformation_matrix[7, 6] = 0.05  # V2 gets component from V1
            transformation_matrix[7, 7] = 0.95  # V2 slightly reduced
            
            # V3-V4: lateral displacement
            transformation_matrix[8, 8] = 0.85  # V3
            transformation_matrix[8, 9] = 0.15  # V3 gets V4 component
            transformation_matrix[9, 8] = 0.1   # V4 gets V3 component
            transformation_matrix[9, 9] = 0.9   # V4
            
            # V5-V6: outward displacement
            transformation_matrix[10, 10] = 0.92 # V5
            transformation_matrix[11, 11] = 0.88 # V6 most affected by lateral displacement
            
        elif displacement_pattern == 'shirt_tight':
            # Tight shirt: more consistent but compressed displacement
            for i in range(6, 12):  # Precordial leads
                transformation_matrix[i, i] = 0.95  # Slight amplitude reduction
                
        elif displacement_pattern == 'shirt_loose':
            # Loose shirt: more variable displacement
            displacement_factors = [0.8, 0.85, 0.75, 0.9, 0.7, 0.65]  # V1-V6
            for i, factor in enumerate(displacement_factors):
                transformation_matrix[i+6, i+6] = factor
                
        return transformation_matrix
    
    def apply_morphological_changes(self, ecg_signal: np.ndarray, 
                                  displacement_vector: Tuple[float, float],
                                  lead_idx: int) -> np.ndarray:
        """
        Apply morphological changes based on electrode displacement.
        
        Args:
            ecg_signal (np.ndarray): Single lead ECG signal (n_samples,)
            displacement_vector (tuple): Displacement in (x, y) coordinates
            lead_idx (int): Lead index (0-11)
            
        Returns:
            np.ndarray: Morphologically altered ECG signal
        """
        lead_names = list(self.lead_positions.keys())
        lead_name = lead_names[lead_idx] if lead_idx < len(lead_names) else f'Lead_{lead_idx}'
        lead_info = self.lead_positions.get(lead_name, {'type': 'precordial', 'vector': [1, 0]})
        
        # Calculate displacement magnitude
        displacement_magnitude = np.sqrt(displacement_vector[0]**2 + displacement_vector[1]**2)
        
        # Get sensitivity factor
        sensitivity = self.displacement_sensitivity[lead_info['type']]
        
        # Apply morphological changes
        altered_signal = ecg_signal.copy()
        
        # 1. Amplitude scaling based on displacement
        amplitude_factor = 1.0 - (displacement_magnitude * sensitivity * 0.3)
        amplitude_factor = np.clip(amplitude_factor, 0.5, 1.5)
        altered_signal *= amplitude_factor
        
        # 2. Phase shift for precordial leads
        if lead_info['type'] == 'precordial':
            phase_shift_samples = int(displacement_vector[0] * 10)  # Max 10 samples shift
            if phase_shift_samples != 0:
                altered_signal = np.roll(altered_signal, phase_shift_samples)
        
        # 3. Morphology distortion (affects QRS complex primarily)
        qrs_regions = self._detect_qrs_regions(altered_signal)
        for start, end in qrs_regions:
            # Apply localized distortion to QRS
            distortion_factor = 1.0 + displacement_magnitude * sensitivity * 0.2
            altered_signal[start:end] *= distortion_factor
        
        return altered_signal
    
    def _detect_qrs_regions(self, ecg_signal: np.ndarray, 
                           threshold_factor: float = 0.3) -> List[Tuple[int, int]]:
        """
        Detect QRS complex regions in ECG signal.
        
        Args:
            ecg_signal (np.ndarray): ECG signal
            threshold_factor (float): Threshold factor for QRS detection
            
        Returns:
            List[Tuple[int, int]]: List of (start, end) indices for QRS regions
        """
        # Simple QRS detection using signal envelope
        analytic_signal = hilbert(ecg_signal)
        envelope = np.abs(analytic_signal)
        
        # Smooth envelope
        window_size = int(0.1 * self.sampling_rate)  # 100ms window
        smoothed_envelope = np.convolve(envelope, np.ones(window_size)/window_size, mode='same')
        
        # Find peaks above threshold
        threshold = threshold_factor * np.max(smoothed_envelope)
        above_threshold = smoothed_envelope > threshold
        
        # Find QRS regions
        qrs_regions = []
        in_qrs = False
        start_idx = 0
        
        for i, above in enumerate(above_threshold):
            if above and not in_qrs:
                start_idx = i
                in_qrs = True
            elif not above and in_qrs:
                qrs_regions.append((start_idx, i))
                in_qrs = False
        
        # Handle case where signal ends while in QRS
        if in_qrs:
            qrs_regions.append((start_idx, len(above_threshold)))
        
        return qrs_regions
    
    def simulate_chest_geometry_variation(self, ecg_signal: np.ndarray,
                                        chest_size_factor: float = 1.0,
                                        heart_position_shift: Tuple[float, float] = (0, 0)) -> np.ndarray:
        """
        Simulate variations in chest geometry and heart position.
        
        Args:
            ecg_signal (np.ndarray): ECG signal of shape (n_leads, n_samples)
            chest_size_factor (float): Chest size scaling factor (0.8-1.2)
            heart_position_shift (tuple): Heart position shift (x, y)
            
        Returns:
            np.ndarray: ECG signal with chest geometry variations
        """
        n_leads, n_samples = ecg_signal.shape
        varied_signal = np.zeros_like(ecg_signal)
        
        for lead_idx in range(n_leads):
            lead_names = list(self.lead_positions.keys())
            lead_name = lead_names[lead_idx] if lead_idx < len(lead_names) else f'Lead_{lead_idx}'
            lead_info = self.lead_positions.get(lead_name, {'type': 'precordial', 'vector': [1, 0]})
            
            # Calculate effective displacement due to chest geometry
            base_vector = np.array(lead_info['vector'])
            
            # Chest size affects electrode distance from heart
            distance_factor = chest_size_factor
            
            # Heart position shift affects all leads differently
            position_effect = np.dot(base_vector, heart_position_shift)
            
            # Combine effects
            amplitude_scaling = (1.0 / distance_factor) * (1.0 + position_effect * 0.2)
            amplitude_scaling = np.clip(amplitude_scaling, 0.5, 2.0)
            
            varied_signal[lead_idx, :] = ecg_signal[lead_idx, :] * amplitude_scaling
        
        return varied_signal
    
    def apply_lead_specific_distortions(self, ecg_signal: np.ndarray,
                                      distortion_profile: Dict[str, float]) -> np.ndarray:
        """
        Apply lead-specific distortions based on shirt electrode positioning.
        
        Args:
            ecg_signal (np.ndarray): ECG signal of shape (n_leads, n_samples)
            distortion_profile (dict): Lead-specific distortion factors
            
        Returns:
            np.ndarray: ECG signal with lead-specific distortions
        """
        n_leads, n_samples = ecg_signal.shape
        distorted_signal = ecg_signal.copy()
        
        lead_names = list(self.lead_positions.keys())
        
        for lead_idx in range(min(n_leads, len(lead_names))):
            lead_name = lead_names[lead_idx]
            
            if lead_name in distortion_profile:
                distortion_factor = distortion_profile[lead_name]
                
                # Apply frequency-dependent distortion
                # High frequencies (QRS) affected more by displacement
                freqs = np.fft.fftfreq(n_samples, 1/self.sampling_rate)
                fft_signal = np.fft.fft(distorted_signal[lead_idx, :])
                
                # Create frequency-dependent filter
                freq_filter = np.ones_like(freqs)
                high_freq_mask = np.abs(freqs) > 10  # Above 10 Hz
                freq_filter[high_freq_mask] *= (1.0 + distortion_factor * 0.3)
                
                # Apply filter and convert back
                filtered_fft = fft_signal * freq_filter
                distorted_signal[lead_idx, :] = np.real(np.fft.ifft(filtered_fft))
        
        return distorted_signal
    
    def apply_combined_anatomical_variations(self, ecg_signal: np.ndarray,
                                           shirt_type: str = 'generic',
                                           chest_size_factor: float = None,
                                           heart_position_shift: Tuple[float, float] = None,
                                           displacement_magnitude: float = None) -> np.ndarray:
        """
        Apply combined anatomical variations for comprehensive simulation.
        
        Args:
            ecg_signal (np.ndarray): ECG signal of shape (n_leads, n_samples)
            shirt_type (str): Type of shirt ('generic', 'tight', 'loose')
            chest_size_factor (float): Chest size factor (random if None)
            heart_position_shift (tuple): Heart position shift (random if None)
            displacement_magnitude (float): Overall displacement magnitude (random if None)
            
        Returns:
            np.ndarray: ECG signal with combined anatomical variations
        """
        # Set random parameters if not provided
        if chest_size_factor is None:
            chest_size_factor = np.random.uniform(0.85, 1.15)
        
        if heart_position_shift is None:
            heart_position_shift = (np.random.uniform(-0.2, 0.2), 
                                  np.random.uniform(-0.2, 0.2))
        
        if displacement_magnitude is None:
            displacement_magnitude = np.random.uniform(0.1, 0.5)
        
        # Apply transformations
        varied_signal = ecg_signal.copy()
        
        # 1. Apply chest geometry variations
        varied_signal = self.simulate_chest_geometry_variation(
            varied_signal, chest_size_factor, heart_position_shift
        )
        
        # 2. Apply lead transformation matrix
        transformation_matrix = self.create_lead_transformation_matrix(f'shirt_{shirt_type}')
        n_leads = min(varied_signal.shape[0], transformation_matrix.shape[0])
        varied_signal[:n_leads, :] = (transformation_matrix[:n_leads, :n_leads] @ 
                                     varied_signal[:n_leads, :])
        
        # 3. Apply morphological changes to each lead
        for lead_idx in range(varied_signal.shape[0]):
            displacement_vector = (
                displacement_magnitude * np.random.uniform(-1, 1),
                displacement_magnitude * np.random.uniform(-1, 1)
            )
            varied_signal[lead_idx, :] = self.apply_morphological_changes(
                varied_signal[lead_idx, :], displacement_vector, lead_idx
            )
        
        # 4. Apply lead-specific distortions
        distortion_profile = self._create_shirt_distortion_profile(shirt_type, displacement_magnitude)
        varied_signal = self.apply_lead_specific_distortions(varied_signal, distortion_profile)
        
        return varied_signal
    
    def _create_shirt_distortion_profile(self, shirt_type: str, 
                                       displacement_magnitude: float) -> Dict[str, float]:
        """
        Create distortion profile based on shirt type and displacement magnitude.
        
        Args:
            shirt_type (str): Type of shirt
            displacement_magnitude (float): Overall displacement magnitude
            
        Returns:
            Dict[str, float]: Lead-specific distortion factors
        """
        base_distortions = {
            'generic': {
                'V1': 0.3, 'V2': 0.4, 'V3': 0.5, 'V4': 0.4, 'V5': 0.6, 'V6': 0.7,
                'I': 0.1, 'II': 0.1, 'III': 0.1, 'aVR': 0.2, 'aVL': 0.2, 'aVF': 0.2
            },
            'tight': {
                'V1': 0.2, 'V2': 0.2, 'V3': 0.3, 'V4': 0.3, 'V5': 0.4, 'V6': 0.4,
                'I': 0.05, 'II': 0.05, 'III': 0.05, 'aVR': 0.1, 'aVL': 0.1, 'aVF': 0.1
            },
            'loose': {
                'V1': 0.5, 'V2': 0.6, 'V3': 0.7, 'V4': 0.6, 'V5': 0.8, 'V6': 0.9,
                'I': 0.2, 'II': 0.2, 'III': 0.2, 'aVR': 0.3, 'aVL': 0.3, 'aVF': 0.3
            }
        }
        
        profile = base_distortions.get(shirt_type, base_distortions['generic'])
        
        # Scale by displacement magnitude
        scaled_profile = {lead: factor * displacement_magnitude 
                         for lead, factor in profile.items()}
        
        return scaled_profile


def create_sample_ecg_with_features(n_leads: int = 12, n_samples: int = 5000, 
                                   sampling_rate: int = 500) -> np.ndarray:
    """
    Create a more realistic synthetic ECG with distinct P, QRS, T features.
    
    Args:
        n_leads (int): Number of ECG leads
        n_samples (int): Number of samples
        sampling_rate (int): Sampling rate in Hz
        
    Returns:
        np.ndarray: Synthetic ECG signal with realistic features
    """
    t = np.arange(n_samples) / sampling_rate
    ecg_signal = np.zeros((n_leads, n_samples))
    
    # Heart rate and timing
    heart_rate = 75  # BPM
    rr_interval = 60 / heart_rate  # seconds
    
    # Lead-specific characteristics
    lead_characteristics = {
        0: {'name': 'I', 'p_amp': 0.1, 'qrs_amp': 0.8, 't_amp': 0.3},      # Lead I
        1: {'name': 'II', 'p_amp': 0.15, 'qrs_amp': 1.2, 't_amp': 0.4},    # Lead II
        2: {'name': 'III', 'p_amp': 0.05, 'qrs_amp': 0.6, 't_amp': 0.2},   # Lead III
        3: {'name': 'aVR', 'p_amp': -0.05, 'qrs_amp': -0.4, 't_amp': -0.1}, # aVR
        4: {'name': 'aVL', 'p_amp': 0.08, 'qrs_amp': 0.5, 't_amp': 0.2},   # aVL
        5: {'name': 'aVF', 'p_amp': 0.12, 'qrs_amp': 1.0, 't_amp': 0.35},  # aVF
        6: {'name': 'V1', 'p_amp': 0.03, 'qrs_amp': -0.5, 't_amp': 0.1},   # V1
        7: {'name': 'V2', 'p_amp': 0.04, 'qrs_amp': 0.3, 't_amp': 0.15},   # V2
        8: {'name': 'V3', 'p_amp': 0.05, 'qrs_amp': 0.8, 't_amp': 0.25},   # V3
        9: {'name': 'V4', 'p_amp': 0.06, 'qrs_amp': 1.5, 't_amp': 0.4},    # V4
        10: {'name': 'V5', 'p_amp': 0.08, 'qrs_amp': 1.3, 't_amp': 0.35},  # V5
        11: {'name': 'V6', 'p_amp': 0.1, 'qrs_amp': 1.1, 't_amp': 0.3}     # V6
    }
    
    for lead_idx in range(min(n_leads, len(lead_characteristics))):
        char = lead_characteristics[lead_idx]
        
        # Generate heartbeats
        signal = np.zeros(n_samples)
        
        # Number of beats in the signal
        n_beats = int(len(t) / (rr_interval * sampling_rate)) + 1
        
        for beat in range(n_beats):
            beat_start_time = beat * rr_interval
            beat_start_idx = int(beat_start_time * sampling_rate)
            
            if beat_start_idx >= n_samples:
                break
            
            # P wave (starts at beat_start)
            p_duration = 0.1  # 100ms
            p_start = beat_start_idx
            p_end = min(p_start + int(p_duration * sampling_rate), n_samples)
            if p_start < n_samples:
                p_indices = np.arange(p_start, p_end)
                p_time = (p_indices - p_start) / sampling_rate
                p_wave = char['p_amp'] * np.exp(-((p_time - p_duration/2) / (p_duration/4))**2)
                signal[p_indices] += p_wave
            
            # QRS complex (starts 120ms after P wave)
            qrs_delay = 0.12  # 120ms PR interval
            qrs_duration = 0.08  # 80ms
            qrs_start = beat_start_idx + int(qrs_delay * sampling_rate)
            qrs_end = min(qrs_start + int(qrs_duration * sampling_rate), n_samples)
            if qrs_start < n_samples:
                qrs_indices = np.arange(qrs_start, qrs_end)
                qrs_time = (qrs_indices - qrs_start) / sampling_rate
                # Complex QRS shape
                qrs_wave = char['qrs_amp'] * (
                    np.sin(2 * np.pi * qrs_time / qrs_duration * 3) * 
                    np.exp(-((qrs_time - qrs_duration/2) / (qrs_duration/6))**2)
                )
                signal[qrs_indices] += qrs_wave
            
            # T wave (starts 200ms after QRS)
            t_delay = 0.20  # 200ms after QRS start
            t_duration = 0.15  # 150ms
            t_start = beat_start_idx + int((qrs_delay + t_delay) * sampling_rate)
            t_end = min(t_start + int(t_duration * sampling_rate), n_samples)
            if t_start < n_samples:
                t_indices = np.arange(t_start, t_end)
                t_time = (t_indices - t_start) / sampling_rate
                t_wave = char['t_amp'] * np.exp(-((t_time - t_duration/2) / (t_duration/4))**2)
                signal[t_indices] += t_wave
        
        # Add baseline noise
        noise = 0.02 * np.random.randn(n_samples)
        signal += noise
        
        ecg_signal[lead_idx, :] = signal
    
    return ecg_signal


# Example usage and demonstration
if __name__ == "__main__":
    # Create sample ECG data with realistic features
    sampling_rate = 500  # Hz
    duration = 10  # seconds
    n_samples = sampling_rate * duration
    n_leads = 12
    
    # Generate realistic synthetic ECG
    original_ecg = create_sample_ecg_with_features(n_leads, n_samples, sampling_rate)
    
    # Initialize anatomical variation simulator
    anatomical_simulator = AnatomicalVariationSimulator(sampling_rate)
    
    print("Anatomical Variation Simulation Demonstration")
    print("=" * 50)
    
    # 1. Basic lead transformation matrix
    print("1. Creating lead transformation matrices...")
    for shirt_type in ['generic', 'tight', 'loose']:
        transform_matrix = anatomical_simulator.create_lead_transformation_matrix(f'shirt_{shirt_type}')
        print(f"   {shirt_type.capitalize()} shirt transformation matrix shape: {transform_matrix.shape}")
        print(f"   Diagonal elements (first 6): {np.diag(transform_matrix)[:6]}")
    
    # 2. Chest geometry variations
    print("\n2. Applying chest geometry variations...")
    chest_sizes = [0.8, 1.0, 1.2]  # Small, normal, large chest
    for chest_size in chest_sizes:
        varied_ecg = anatomical_simulator.simulate_chest_geometry_variation(
            original_ecg, 
            chest_size_factor=chest_size,
            heart_position_shift=(0.1, -0.05)
        )
        amplitude_change = np.mean(np.std(varied_ecg, axis=1)) / np.mean(np.std(original_ecg, axis=1))
        print(f"   Chest size factor {chest_size}: amplitude ratio = {amplitude_change:.3f}")
    
    # 3. Morphological changes for individual leads
    print("\n3. Applying morphological changes...")
    test_lead = original_ecg[8, :]  # V3 lead
    displacement_vectors = [(0.1, 0.05), (0.2, 0.1), (0.3, 0.15)]
    
    for i, displacement in enumerate(displacement_vectors):
        morphed_lead = anatomical_simulator.apply_morphological_changes(
            test_lead, displacement, lead_idx=8
        )
        correlation = np.corrcoef(test_lead, morphed_lead)[0, 1]
        print(f"   Displacement {displacement}: correlation with original = {correlation:.3f}")
    
    # 4. Lead-specific distortions
    print("\n4. Applying lead-specific distortions...")
    distortion_profiles = {
        'mild': {'V1': 0.1, 'V2': 0.15, 'V3': 0.2, 'V4': 0.15, 'V5': 0.25, 'V6': 0.3},
        'moderate': {'V1': 0.3, 'V2': 0.4, 'V3': 0.5, 'V4': 0.4, 'V5': 0.6, 'V6': 0.7},
        'severe': {'V1': 0.5, 'V2': 0.6, 'V3': 0.8, 'V4': 0.6, 'V5': 0.9, 'V6': 1.0}
    }
    
    for profile_name, profile in distortion_profiles.items():
        distorted_ecg = anatomical_simulator.apply_lead_specific_distortions(original_ecg, profile)
        mse = np.mean((original_ecg - distorted_ecg)**2)
        print(f"   {profile_name.capitalize()} distortion: MSE = {mse:.6f}")
    
    # 5. Combined anatomical variations
    print("\n5. Applying combined anatomical variations...")
    shirt_types = ['generic', 'tight', 'loose']
    
    for shirt_type in shirt_types:
        combined_varied_ecg = anatomical_simulator.apply_combined_anatomical_variations(
            original_ecg,
            shirt_type=shirt_type,
            chest_size_factor=np.random.uniform(0.9, 1.1),
            heart_position_shift=(np.random.uniform(-0.1, 0.1), np.random.uniform(-0.1, 0.1)),
            displacement_magnitude=np.random.uniform(0.2, 0.4)
        )
        
        # Calculate metrics
        snr_original = np.mean(np.var(original_ecg, axis=1)) / np.var(original_ecg - np.mean(original_ecg))
        snr_varied = np.mean(np.var(combined_varied_ecg, axis=1)) / np.var(combined_varied_ecg - np.mean(combined_varied_ecg))
        
        print(f"   {shirt_type.capitalize()} shirt variation:")
        print(f"     Original signal shape: {original_ecg.shape}")
        print(f"     Varied signal shape: {combined_varied_ecg.shape}")
        print(f"     SNR ratio (varied/original): {snr_varied/snr_original:.3f}")
    
    # 6. Batch processing demonstration
    print("\n6. Batch processing demonstration...")
    batch_size = 3
    batch_ecg = np.stack([create_sample_ecg_with_features(n_leads, n_samples, sampling_rate) 
                          for _ in range(batch_size)])
    print(f"   Created batch of {batch_size} ECG signals: {batch_ecg.shape}")
    
    # Apply different variations to each sample
    shirt_types_batch = ['generic', 'tight', 'loose']
    varied_batch = []
    
    for i in range(batch_size):
        varied_sample = anatomical_simulator.apply_combined_anatomical_variations(
            batch_ecg[i],
            shirt_type=shirt_types_batch[i],
            chest_size_factor=np.random.uniform(0.85, 1.15),
            displacement_magnitude=np.random.uniform(0.1, 0.5)
        )
        varied_batch.append(varied_sample)
    
    varied_batch = np.stack(varied_batch)
    print(f"   Processed batch shape: {varied_batch.shape}")
    
    # Calculate batch statistics
    original_batch_std = np.mean([np.std(batch_ecg[i]) for i in range(batch_size)])
    varied_batch_std = np.mean([np.std(varied_batch[i]) for i in range(batch_size)])
    print(f"   Average std - Original: {original_batch_std:.4f}, Varied: {varied_batch_std:.4f}")
    
    print("\n7. QRS Detection demonstration...")
    # Test QRS detection on a sample lead
    test_signal = original_ecg[1, :]  # Lead II
    qrs_regions = anatomical_simulator._detect_qrs_regions(test_signal)
    print(f"   Detected {len(qrs_regions)} QRS complexes in Lead II")
    print(f"   QRS regions (sample indices): {qrs_regions[:3]}...")  # Show first 3


"""
EXPLANATION OF ANATOMICAL VARIATION SIMULATION:

This module simulates anatomical variations and electrode displacement effects
that occur when using shirt-based ECG systems compared to standard hospital ECG placement.

KEY CONCEPTS:

1. LEAD TRANSFORMATION MATRICES:
   - Model how electrode displacement affects inter-lead relationships
   - Different patterns for different shirt types (tight, loose, generic)
   - Precordial leads (V1-V6) most affected by chest placement variations
   - Limb leads less affected by shirt-based displacement

2. MORPHOLOGICAL CHANGES:
   - Simulate how electrode displacement alters ECG waveform morphology
   - QRS complexes most sensitive to spatial displacement
   - Phase shifts and amplitude changes based on displacement vectors
   - Lead-specific sensitivity factors based on anatomical positioning

3. CHEST GEOMETRY VARIATIONS:
   - Account for different body sizes and chest configurations
   - Heart position variations relative to electrode positions
   - Distance-dependent amplitude scaling (inverse relationship)
   - Individual anatomical differences in heart-electrode geometry

4. LEAD-SPECIFIC DISTORTIONS:
   - Frequency-dependent distortions (high frequencies more affected)
   - Shirt-type specific distortion profiles
   - Realistic modeling of contact quality variations
   - Differential effects on different ECG leads

5. QRS DETECTION:
   - Automated detection of QRS complexes for targeted morphological changes
   - Uses Hilbert transform for envelope detection
   - Enables localized distortions during most critical cardiac events
   - Maintains physiological validity of transformations

PHYSIOLOGICAL BASIS:
- Precordial leads (V1-V6) show greatest sensitivity to chest displacement
- Limb leads (I, II, III) relatively stable with chest electrode movement
- Augmented leads (aVR, aVL, aVF) show intermediate sensitivity
- QRS morphology changes significantly with electrode displacement
- T-wave and P-wave changes are typically less dramatic

USAGE FOR WEARABLE ECG:
- Simulates realistic electrode displacement in fabric-based systems
- Models varying contact quality and impedance changes
- Accounts for body movement and clothing fit variations
- Provides training data that bridges hospital-to-wearable domain gap

The transformations maintain ECG diagnostic validity while introducing
realistic variations expected in shirt-based monitoring systems.
"""
        
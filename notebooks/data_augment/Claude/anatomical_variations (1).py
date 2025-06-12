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
        
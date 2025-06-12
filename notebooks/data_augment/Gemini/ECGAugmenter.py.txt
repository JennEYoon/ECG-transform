import numpy as np
import torch

class ECGAugmenter:
    """
    A class to apply realistic augmentations to 12-lead ECG data based on
    the "ECG Data Augmentation Strategy for Prototype Device" document.

    This class simulates two main types of real-world imperfections:
    1. Lead Displacement: Simulates physical shifts of electrodes.
    2. Noise: Adds various types of noise common in wearable devices.

    Args:
        sampling_rate (int): The sampling rate of the ECG signals (e.g., 500 Hz).
        lead_names (list): A list of 12 lead names in the correct order.
                           Example: ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 
                                     'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
    """
    def __init__(self, sampling_rate=500, lead_names=None):
        self.sampling_rate = sampling_rate
        if lead_names is None:
            self.lead_names = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
        else:
            self.lead_names = lead_names
            
        # Create a mapping from lead name to index for easy lookup
        self.lead_map = {name: i for i, name in enumerate(self.lead_names)}

    def _get_lead(self, ecg, lead_name):
        """Helper to get a lead by name."""
        return ecg[self.lead_map[lead_name], :]

    def _set_lead(self, ecg, lead_name, data):
        """Helper to set a lead by name."""
        ecg[self.lead_map[lead_name], :] = data

    def simulate_lead_displacement(self, ecg):
        """
        Simulates the physical displacement of ECG electrodes by mixing signals
        from adjacent leads. This is Stage 1 of the augmentation pipeline.

        Args:
            ecg (np.ndarray): A 12-lead ECG signal of shape (12, num_samples).

        Returns:
            np.ndarray: The ECG signal with simulated lead displacement.
        """
        displaced_ecg = ecg.copy()

        # --- 1. Limb Leads Augmentation ---
        # Augment leads I and II, then recalculate the rest.
        alpha = np.random.uniform(-0.1, 0.1)
        beta = np.random.uniform(-0.1, 0.1)

        I = self._get_lead(ecg, 'I')
        II = self._get_lead(ecg, 'II')
        
        # II_aug = (1 - α) * II + α * I
        II_aug = (1 - alpha) * II + alpha * I
        # I_aug = (1 - β) * I + β * II
        I_aug = (1 - beta) * I + beta * II
        
        self._set_lead(displaced_ecg, 'I', I_aug)
        self._set_lead(displaced_ecg, 'II', II_aug)

        # Recalculate dependent limb leads based on the augmented I and II
        # III = II - I
        self._set_lead(displaced_ecg, 'III', self._get_lead(displaced_ecg, 'II') - self._get_lead(displaced_ecg, 'I'))
        # aVR = -(I + II) / 2
        self._set_lead(displaced_ecg, 'aVR', -(self._get_lead(displaced_ecg, 'I') + self._get_lead(displaced_ecg, 'II')) / 2)
        # aVL = I - II / 2
        self._set_lead(displaced_ecg, 'aVL', self._get_lead(displaced_ecg, 'I') - self._get_lead(displaced_ecg, 'II') / 2)
        # aVF = II - I / 2
        self._set_lead(displaced_ecg, 'aVF', self._get_lead(displaced_ecg, 'II') - self._get_lead(displaced_ecg, 'I') / 2)
        
        # --- 2. Precordial Leads Augmentation ---
        # V1 is mixed with V2
        alpha_v1 = np.random.uniform(0, 0.15)
        v1_aug = (1 - alpha_v1) * self._get_lead(ecg, 'V1') + alpha_v1 * self._get_lead(ecg, 'V2')
        self._set_lead(displaced_ecg, 'V1', v1_aug)

        # Leads V2 to V5 are mixed with their two neighbors
        for i in range(2, 6):
            lead_name = f'V{i}'
            prev_lead = f'V{i-1}'
            next_lead = f'V{i+1}'
            
            alpha = np.random.uniform(0, 0.15)
            beta = np.random.uniform(0, 0.15)
            # Ensure coefficients don't sum to > 1
            if alpha + beta > 1:
                # Simple scaling to keep it within bounds while preserving ratio
                total = alpha + beta
                alpha /= total
                beta /= total

            v_orig = self._get_lead(ecg, lead_name)
            v_prev = self._get_lead(ecg, prev_lead)
            v_next = self._get_lead(ecg, next_lead)
            
            v_aug = (1 - alpha - beta) * v_orig + alpha * v_prev + beta * v_next
            self._set_lead(displaced_ecg, lead_name, v_aug)

        # V6 is mixed with V5
        alpha_v6 = np.random.uniform(0, 0.15)
        v6_aug = (1 - alpha_v6) * self._get_lead(ecg, 'V6') + alpha_v6 * self._get_lead(ecg, 'V5')
        self._set_lead(displaced_ecg, 'V6', v6_aug)

        return displaced_ecg

    def simulate_noise(self, ecg):
        """
        Adds various types of realistic noise to the ECG signal.
        This is Stage 2 of the augmentation pipeline.

        Args:
            ecg (np.ndarray): A 12-lead ECG signal of shape (12, num_samples).

        Returns:
            np.ndarray: The ECG signal with added noise.
        """
        noisy_ecg = ecg.copy()
        num_samples = ecg.shape[1]
        
        # Apply each noise type with a certain probability
        if np.random.rand() < 0.5: # 50% chance to add baseline wander
            noisy_ecg = self.add_baseline_wander(noisy_ecg)
            
        if np.random.rand() < 0.5: # 50% chance to add powerline interference
            noisy_ecg = self.add_powerline_interference(noisy_ecg)
            
        if np.random.rand() < 0.5: # 50% chance to add muscle artifacts
            noisy_ecg = self.add_muscle_artifacts(noisy_ecg)
            
        if np.random.rand() < 0.3: # 30% chance to add motion artifacts
            noisy_ecg = self.add_motion_artifacts(noisy_ecg)
            
        return noisy_ecg

    def add_baseline_wander(self, ecg):
        """Adds low-frequency sine wave noise to simulate breathing."""
        num_samples = ecg.shape[1]
        t = np.arange(num_samples) / self.sampling_rate
        
        for i in range(ecg.shape[0]): # Apply to each lead
            # Get signal amplitude to scale the noise appropriately
            signal_amplitude = np.max(ecg[i, :]) - np.min(ecg[i, :])
            if signal_amplitude == 0: continue
            
            # Random frequency for breathing (e.g., 0.05 Hz to 0.5 Hz)
            freq = np.random.uniform(0.05, 0.5)
            # Random amplitude, e.g., 5-15% of signal amplitude
            amplitude = np.random.uniform(0.05, 0.15) * signal_amplitude
            phase = np.random.uniform(0, 2 * np.pi)
            
            wander = amplitude * np.sin(2 * np.pi * freq * t + phase)
            ecg[i, :] += wander
        return ecg

    def add_powerline_interference(self, ecg, powerline_freq=60.0):
        """Adds powerline noise (50 or 60 Hz)."""
        num_samples = ecg.shape[1]
        t = np.arange(num_samples) / self.sampling_rate
        
        for i in range(ecg.shape[0]):
            signal_amplitude = np.max(ecg[i, :]) - np.min(ecg[i, :])
            if signal_amplitude == 0: continue
            
            # Amplitude is typically small, e.g., 1-5% of signal amplitude
            amplitude = np.random.uniform(0.01, 0.05) * signal_amplitude
            phase = np.random.uniform(0, 2 * np.pi)
            
            powerline_noise = amplitude * np.sin(2 * np.pi * powerline_freq * t + phase)
            ecg[i, :] += powerline_noise
        return ecg

    def add_muscle_artifacts(self, ecg):
        """Adds high-frequency Gaussian noise to simulate EMG/muscle artifacts."""
        for i in range(ecg.shape[0]):
            signal_amplitude = np.max(ecg[i, :]) - np.min(ecg[i, :])
            if signal_amplitude == 0: continue

            # Noise standard deviation as a fraction of signal amplitude
            sigma = np.random.uniform(0.02, 0.07) * signal_amplitude
            noise = np.random.normal(0, sigma, ecg.shape[1])
            ecg[i, :] += noise
        return ecg

    def add_motion_artifacts(self, ecg):
        """Adds sudden, sharp spikes or baseline shifts."""
        num_samples = ecg.shape[1]
        
        num_artifacts = np.random.randint(1, 4) # Add 1 to 3 artifacts
        
        for _ in range(num_artifacts):
            artifact_type = np.random.choice(['spike', 'shift'])
            
            for i in range(ecg.shape[0]): # Apply to all leads consistently
                signal_amplitude = np.max(ecg[i, :]) - np.min(ecg[i, :])
                if signal_amplitude == 0: continue
                
                pos = np.random.randint(0, num_samples)
                
                if artifact_type == 'spike':
                    # Sharp Gaussian spike
                    amplitude = np.random.uniform(0.2, 0.8) * signal_amplitude
                    width = np.random.randint(self.sampling_rate // 50, self.sampling_rate // 10)
                    spike = amplitude * np.exp(-((np.arange(num_samples) - pos)**2) / (2 * (width**2)))
                    if np.random.rand() < 0.5: spike *= -1 # Random polarity
                    ecg[i, :] += spike
                
                elif artifact_type == 'shift':
                    # Baseline shift
                    magnitude = np.random.uniform(0.1, 0.4) * signal_amplitude
                    if np.random.rand() < 0.5: magnitude *= -1
                    ecg[i, pos:] += magnitude
        return ecg

    def augment(self, ecg):
        """
        Applies the full two-stage augmentation pipeline to an ECG signal.

        Args:
            ecg (np.ndarray or torch.Tensor): A 12-lead ECG signal of shape 
                                              (12, num_samples).

        Returns:
            np.ndarray or torch.Tensor: The fully augmented ECG signal.
        """
        # Ensure input is a numpy array for processing
        is_torch = isinstance(ecg, torch.Tensor)
        if is_torch:
            original_device = ecg.device
            ecg_np = ecg.cpu().numpy()
        else:
            ecg_np = ecg.copy()

        # --- STAGE 1: SIMULATE LEAD DISPLACEMENT ---
        displaced_ecg = self.simulate_lead_displacement(ecg_np)

        # --- STAGE 2: SIMULATE NOISE ---
        augmented_ecg = self.simulate_noise(displaced_ecg)

        # Convert back to torch.Tensor if that was the original type
        if is_torch:
            return torch.from_numpy(augmented_ecg).float().to(original_device)
        
        return augmented_ecg


if __name__ == '__main__':
    # --- Example Usage ---
    SAMPLING_RATE = 500  # Hz
    SIGNAL_LENGTH = 10   # seconds
    NUM_SAMPLES = SAMPLING_RATE * SIGNAL_LENGTH
    
    # 1. Create a dummy 12-lead ECG signal (e.g., a combination of sine waves)
    print("Creating a dummy 12-lead ECG signal...")
    t = np.linspace(0, SIGNAL_LENGTH, NUM_SAMPLES)
    # Create a base signal with a few frequencies to simulate P, QRS, T waves
    base_signal = (1.0 * np.sin(2 * np.pi * 1 * t) +       # P-T wave component
                   0.2 * np.sin(2 * np.pi * 10 * t) +      # QRS-like component
                   0.05 * np.sin(2 * np.pi * 20 * t))      # Fine details
    
    # Create a 12-lead signal by slightly varying the base signal
    original_ecg = np.zeros((12, NUM_SAMPLES))
    for i in range(12):
        original_ecg[i, :] = base_signal * (1 + (i - 6) * 0.05) # Small variation per lead
        
    print(f"Original ECG shape: {original_ecg.shape}")

    # 2. Initialize the augmenter
    augmenter = ECGAugmenter(sampling_rate=SAMPLING_RATE)

    # 3. Apply the augmentation
    print("\nApplying augmentation...")
    augmented_ecg_np = augmenter.augment(original_ecg)
    print(f"Augmented ECG shape: {augmented_ecg_np.shape}")

    # Example with a PyTorch tensor
    print("\nApplying augmentation to a PyTorch tensor...")
    original_ecg_torch = torch.from_numpy(original_ecg).float()
    augmented_ecg_torch = augmenter.augment(original_ecg_torch)
    print(f"Augmented PyTorch tensor shape: {augmented_ecg_torch.shape}")
    
    # 4. (Optional) Visualize the results to see the difference
    try:
        import matplotlib.pyplot as plt
        
        lead_to_plot = 'II'
        lead_idx = augmenter.lead_map[lead_to_plot]
        
        fig, axes = plt.subplots(2, 1, figsize=(15, 8), sharex=True)
        fig.suptitle(f'ECG Augmentation Example (Lead {lead_to_plot})', fontsize=16)
        
        axes[0].plot(t, original_ecg[lead_idx, :], color='blue', label='Original')
        axes[0].set_title('Original Signal')
        axes[0].grid(True, linestyle='--', alpha=0.6)
        axes[0].legend()
        axes[0].set_ylabel('Amplitude (mV)')
        
        axes[1].plot(t, augmented_ecg_np[lead_idx, :], color='red', label='Augmented')
        axes[1].set_title('Augmented Signal')
        axes[1].grid(True, linestyle='--', alpha=0.6)
        axes[1].legend()
        axes[1].set_xlabel('Time (s)')
        axes[1].set_ylabel('Amplitude (mV)')

        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show()

    except ImportError:
        print("\nMatplotlib not found. Skipping visualization.")
        print("To visualize the result, install it: pip install matplotlib")

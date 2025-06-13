# Pan-Tompkins ECG Signal Processing
This repository provides an implementation of the Pan-Tompkins algorithm for detecting R-peaks in an ECG (Electrocardiogram) signal. This algorithm performs preprocessing, filtering, differentiation, squaring, moving average filtering, and peak detection on ECG data. The main code performs these steps on ECG data from the MIT-BIH Arrhythmia Database.

The Pan-Tompkins algorithm is a well-known method for detecting QRS complexes, specifically R-peaks, in ECG signals. This code uses several steps to preprocess the signal and identify R-peaks, which are critical for further analysis of heart rate variability, arrhythmia detection, and more.

## Code Structure
- Loading the Signal: Load the raw ECG signal from the MIT-BIH dataset.
- Pan-Tompkins Algorithm:
- Bandpass Filtering: Removes noise and baseline drift.
- Differentiation: Emphasizes slope information of the QRS complex.
- Squaring: Amplifies larger differences and makes all values positive.
- Moving Average Filter: Smooths the squared signal over a short window to detect peaks.
- Peak Detection: Finds R-peaks using a height threshold and minimum distance between peaks.


## ECG Signal Processing Steps
### 1. Load ECG Signal
Loads the signal data and extracts the first 10,000 samples.

### 2. Bandpass Filtering
Applies a 0.5–20 Hz bandpass filter to reduce baseline drift and high-frequency noise, which prepares the signal for further processing.

### 3.Differentiation
Computes the derivative of the filtered signal to highlight rapid changes associated with the QRS complex.

### 4. Squaring
Squares the differentiated signal, enhancing QRS complexes while attenuating smaller signal components.

### 5. Moving Average Filter
Uses a Hamming window (150 ms) to smooth the squared signal, making R-peaks more distinguishable.

### 6.Peak Detection
Detects R-peaks using a peak-finding algorithm with specified thresholds for height and distance between peaks, marking each R-peak location on both the moving average and the original signal.


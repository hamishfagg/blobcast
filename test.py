import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Constants
sampling_frequency = 22000  # in Hz
cutoff_frequency = 8000  # in Hz
order = 3  # Filter order
ripple = 1  # Ripple in dB for the Chebyshev filter

# Normalize the frequency to Nyquist Frequency (half of the sampling rate)
normalized_cutoff = cutoff_frequency / (0.5 * sampling_frequency)

# Butterworth Filter Design
butter_b, butter_a = signal.butter(order, normalized_cutoff, btype="low", analog=False)
w_butter, h_butter = signal.freqz(butter_b, butter_a, worN=8000)

# Chebyshev Type I Filter Design
cheby_b, cheby_a = signal.cheby1(
    order, ripple, normalized_cutoff, btype="low", analog=False
)
w_cheby, h_cheby = signal.freqz(cheby_b, cheby_a, worN=8000)

# Plotting in dark mode with the adjusted gain axis
plt.style.use("dark_background")
plt.figure(figsize=(10, 6))

# Plot frequency responses
plt.semilogx(
    0.5 * sampling_frequency * w_butter / np.pi,
    20 * np.log10(np.abs(h_butter)),
    label="Butterworth",
)
plt.semilogx(
    0.5 * sampling_frequency * w_cheby / np.pi,
    20 * np.log10(np.abs(h_cheby)),
    label="Chebyshev Type I",
)

# Add a marker for the cutoff frequency
plt.axvline(
    cutoff_frequency, color="red", linestyle="--", label="Cutoff Frequency (8 kHz)"
)

# Add a marker for the -3 dB point at the cutoff frequency
plt.axhline(-3, color="green", linestyle="--", label="-3 dB")

plt.title("Butterworth and Chebyshev Filter Frequency Responses")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Gain (dB)")
plt.xlim(3000, 13000)  # Frequency range around 8 kHz ± 5 kHz
plt.ylim(-50, 2)  # Gain from +2 to -50 dB (inverted)
plt.grid(which="both", linestyle="-", color="gray", alpha=0.7)

# Adding filter parameters to the plot
plt.text(
    3500,
    -10,
    f"Butterworth\nOrder: {order}\nCutoff: {cutoff_frequency} Hz",
    bbox=dict(facecolor="white", alpha=0.8),
)
plt.text(
    3500,
    -30,
    f"Chebyshev I\nOrder: {order}\nRipple: {ripple} dB\nCutoff: {cutoff_frequency} Hz",
    bbox=dict(facecolor="white", alpha=0.8),
)

plt.legend()
plt.tight_layout()
plt.show()

# Resetting to default style after plot
plt.style.use("default")
from __future__ import division

import numpy as np
import matplotlib.pyplot as plt
import wave

fL = 0.1  # Cutoff frequency as a fraction of the sampling rate (in (0, 0.5)).
fH = 0.4  # Cutoff frequency as a fraction of the sampling rate (in (0, 0.5)).
b = 0.08  # Transition band, as a fraction of the sampling rate (in (0, 0.5)).
N = int(np.ceil((4 / b)))
if not N % 2:
    N += 1  # Make sure that N is odd.
n = np.arange(N)

# Compute a low-pass filter with cutoff frequency fH.
hlpf = np.sinc(2 * fH * (n - (N - 1) / 2))
hlpf *= np.blackman(N)
hlpf = hlpf / np.sum(hlpf)

# Compute a high-pass filter with cutoff frequency fL.
hhpf = np.sinc(2 * fL * (n - (N - 1) / 2))
hhpf *= np.blackman(N)
hhpf = hhpf / np.sum(hhpf)
hhpf = -hhpf
hhpf[(N - 1) // 2] += 1

# Convolve both filters.
h = np.convolve(hlpf, hhpf)

# Audio Import
audio = wave.open("clip1.wav", "rb")
sampleRate = audio.getframerate()
awpWidth = audio.getsampwidth()
nChannels = audio.getnchannels()
nFrames = audio.getnframes()
signal = np.sum(np.fromstring(audio.readframes(nFrames * nChannels), dtype=np.int16).reshape(audio.getnframes(), audio.getnchannels()).T, axis=0)/2

# TODO: FTT the Signal

# TODO: Apply filter to signal

# TODO: iFFT the signal

wave_file = wave.open("result_bp.wav", "wb")
wave_file.setparams((1, awpWidth, sampleRate, nFrames, audio.getcomptype(), audio.getcompname()))
# wave_file.setparams(audio.getparams())
wave_file.writeframes(mod_signal.tobytes("C"))

audio.close()
wave_file.close()

# dummy_audio = np.ones(100)
# mod_audio = np.convolve(dummy_audio, h)
# plt.plot(mod_audio)
# plt.show()
print("Here")
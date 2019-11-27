import pydub
from scipy.signal import butter, sosfilt
import wave
import math
import numpy as np
import matplotlib.pyplot as plt
import os
import struct
import audioop

def running_mean(x, windowSize):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[windowSize:] - cumsum[:-windowSize]) / windowSize


# from http://stackoverflow.com/questions/2226853/interpreting-wav-data/2227174#2227174
def interpret_wav(raw_bytes, n_frames, n_channels, sample_width, interleaved=True):
    if sample_width == 1:
        dtype = np.uint8  # unsigned char
    elif sample_width == 2:
        dtype = np.int16  # signed 2-byte short
    else:
        raise ValueError("Only supports 8 and 16 bit audio formats.")

    channels = np.fromstring(raw_bytes, dtype=dtype)

    if interleaved:
        # channels are interleaved, i.e. sample N of channel M follows sample N of channel M-1 in raw data
        channels.shape = (n_frames, n_channels)
        channels = channels.T
    else:
        # channels are not interleaved. All samples from channel M occur before all samples from channel M-1
        channels.shape = (n_channels, n_frames)

    return channels


audio = wave.open("clip1.wav", "rb")
sampleRate = audio.getframerate()
awpWidth = audio.getsampwidth()
nChannels = audio.getnchannels()
nFrames = audio.getnframes()

signal = audio.readframes(nFrames * nChannels)
channels = interpret_wav(signal, nFrames, nChannels, awpWidth, True)

# Original
cutoff = sampleRate  # Hz
freqRatio = cutoff / sampleRate
N = int(math.sqrt(0.196196 + freqRatio ** 2) / freqRatio)

orig = running_mean(channels[0], N).astype(channels.dtype)
orig1 = running_mean(channels[1], N).astype(channels.dtype)
original = (orig * 0.5 + orig1 * 0.5).astype(np.int16)

# Low Pass
cutoff = 11000  # Hz
freqRatio = cutoff / sampleRate
N = int(math.sqrt(0.196196 + freqRatio ** 2) / freqRatio)

filtered = running_mean(channels[0], N).astype(channels.dtype)
filtered1 = running_mean(channels[1], N).astype(channels.dtype)
sterio = (filtered * 0.5 + filtered1 * 0.5).astype(np.int16)

# Invert to High Pass
mod_audio = original[0:sterio.shape[0]] - sterio

if os.path.exists("result_hp.wav"):
    os.remove("result_hp.wav")

wave_file = wave.open("result_hp.wav", "wb")
wave_file.setparams((1, awpWidth, sampleRate, nFrames, audio.getcomptype(), audio.getcompname()))
wave_file.writeframes(audioop.mul(mod_audio.tobytes("C"), audio.getsampwidth(), 1.2))


audio.close()
wave_file.close()

print("Here")

##############################################################
#   Libraries
##############################################################
import wave
import math
import numpy as np
import os
import audioop
import pyaudio


##############################################################
#   Variable Definition
##############################################################
VOL_MULTI = 1.1


##############################################################
#   Class Definition
##############################################################
class FilterType:
    def __init__(self, audio, mod_audio):
        self.filter = True
        self.audio = audio
        self.sample_rate = audio.getframerate()
        self.awp_width = audio.getsampwidth()
        self.n_channels = audio.getnchannels()
        self.n_frames = audio.getnframes()
        self.signal = mod_audio

    def low_pass_filter(self, signal=None, frequency=10,
                        save_result=False, internal_return=False, play=False, file_name="result_lp.wav"):
        # Calculate Running Mean
        def running_mean(x, window_size):
            cumsum = np.cumsum(np.insert(x, 0, 0))
            return (cumsum[window_size:] - cumsum[:-window_size]) / window_size

        # Interpreting the wave file
        def interpret_wav(raw_bytes, n_frames, n_channels, sample_width, interleaved=True):
            if sample_width == 1:
                data_type = np.uint8  # unsigned char
            elif sample_width == 2:
                data_type = np.int16  # signed 2-byte short
            else:
                raise ValueError("Only supports 8 and 16 bit audio formats.")
            # Obtain Original Audio in bytes
            channel_box = np.fromstring(raw_bytes, dtype=data_type)
            if interleaved:
                # Allocate Audio to their channels
                # channels are interleaved, i.e. sample N of channel M follows sample N of channel M-1 in raw data
                channel_box.shape = (n_frames, n_channels)
                channel_box = channel_box.T
            else:
                # channels are not interleaved. All samples from channel M occur before all samples from channel M-1
                channel_box.shape = (n_channels, n_frames)
            # Return Value
            return channel_box

        # Low Pass Filter
        if not signal:
            signal = self.signal
        else:
            pass
        channels = interpret_wav(signal, self.n_frames, self.n_channels, self.awp_width, True)
        # Casting the Filter
        cutoff = frequency
        freq_ratio = cutoff / self.sample_rate
        window = int(math.sqrt(0.196196 + freq_ratio ** 2) / freq_ratio)
        # Dual Channel Audio Modification
        filtered = running_mean(channels[0], window).astype(channels.dtype)
        if self.n_frames == 2:
            filtered1 = running_mean(channels[1], window).astype(channels.dtype)
            stereo = (filtered * 0.5 + filtered1 * 0.5).astype(np.int16)
        else:
            stereo = filtered.astype(np.int16)
        # Save Return Value
        if internal_return:
            mod_signal = stereo
        else:
            mod_signal = stereo.tobytes("C")
            self.n_frames = stereo.shape[0]
            self.n_channels = 1
        # Extra Step
        if save_result:
            # Remove old file
            if os.path.exists(file_name):
                os.remove(file_name)
            # Create New File
            wave_file = wave.open(file_name, "wb")
            wave_file.setparams((1, self.awp_width, self.sample_rate, self.n_frames,
                                 self.audio.getcomptype(), self.audio.getcompname()))
            wave_file.writeframes(audioop.mul(mod_signal, self.audio.getsampwidth(), VOL_MULTI))
            wave_file.close()
        if play:
            # Initialize pyaudio
            p = pyaudio.PyAudio()
            # Open Stream
            stream = p.open(format=p.get_format_from_width(self.awp_width),
                            channels=self.n_channels,
                            rate=self.sample_rate,
                            output=True)
            # Play Stream
            stream.write(frames=stereo, num_frames=None)
            # Stop Stream
            stream.stop_stream()
            stream.close()
            p.terminate()
        # Return Result
        return mod_signal

    def high_pass_filter(self, signal=None, frequency=10, save_result=False, play=False, file_name="result_hp.wav"):
        if not signal:
            signal = self.signal
        else:
            pass
        # Old data
        original = self.low_pass_filter(signal=signal, frequency=self.audio.getframerate(),
                                        save_result=False, internal_return=True, play=False)
        low_passed = self.low_pass_filter(signal=signal, frequency=frequency,
                                          save_result=False, internal_return=True, play=False)
        # High Passed Data
        high_passed = original[0:low_passed.shape[0]] - low_passed
        # Save Return Value
        mod_audio = high_passed.tobytes("C")
        # Extra Step
        if save_result:
            # Remove old file
            if os.path.exists(file_name):
                os.remove(file_name)
            # Create New File
            wave_file = wave.open(file_name, "wb")
            wave_file.setparams((1, self.awp_width, self.sample_rate, self.n_frames,
                                 self.audio.getcomptype(), self.audio.getcompname()))
            wave_file.writeframes(audioop.mul(mod_audio, self.audio.getsampwidth(), VOL_MULTI))
            wave_file.close()
        if play:
            # Initialize pyaudio
            p = pyaudio.PyAudio()
            # Open Stream
            stream = p.open(format=p.get_format_from_width(self.awp_width),
                            channels=self.n_channels,
                            rate=self.sample_rate,
                            output=True)
            # Play Stream
            stream.write(frames=mod_audio, num_frames=None)
            # Stop Stream
            stream.stop_stream()
            stream.close()
            p.terminate()
        # Return Result
        self.n_frames = high_passed.shape[0]
        self.n_channels = 1
        return mod_audio

    def band_pass_filter(self, low_frequency, high_frequency, save_result=False, play=False, file_name="result_bp.wav"):
        # Low Pass
        low_passed = self.low_pass_filter(frequency=high_frequency, save_result=False,
                                          internal_return=False, play=False)
        # High Pass
        band_passed = self.high_pass_filter(signal=low_passed, frequency=low_frequency,
                                            save_result=False, play=False)
        # Extra Step
        if save_result:
            if file_name.lower().endswith(".wav"):
                pass
            else:
                file_name = file_name + ".wav"
            # Remove old file
            if os.path.exists(file_name):
                os.remove(file_name)
            # Create New File
            wave_file = wave.open(file_name, "wb")
            wave_file.setparams((1, self.awp_width, self.sample_rate, self.n_frames,
                                 self.audio.getcomptype(), self.audio.getcompname()))
            wave_file.writeframes(audioop.mul(band_passed, self.audio.getsampwidth(), VOL_MULTI))
            wave_file.close()
        if play:
            print("  Now Playing Equalized Audio...")
            # Initialize pyaudio
            p = pyaudio.PyAudio()
            # Open Stream
            stream = p.open(format=p.get_format_from_width(self.awp_width),
                            channels=self.n_channels,
                            rate=self.sample_rate,
                            output=True)
            # Play Stream
            stream.write(frames=band_passed, num_frames=None)
            # Stop Stream
            stream.stop_stream()
            stream.close()
            p.terminate()
        # Return Result
        return [band_passed, self.n_frames]


##############################################################
#   Function Prototype
##############################################################
def test():
    audio = wave.open("clip1.wav", "rb")
    filtering = FilterType(audio=audio, mod_audio=audio.readframes(-1))
    mod_audio = filtering.band_pass_filter(low_frequency=60, high_frequency=250, save_result=True, play=False)


##############################################################
#   Main Function
##############################################################
def main():
    print("Hello World!")
    test()


##############################################################
#    Main Function Runner
##############################################################
if __name__ == "__main__":
    main()
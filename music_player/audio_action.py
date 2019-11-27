##############################################################
#   Libraries
##############################################################
import numpy as np
import os
import subprocess
import wave
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile
from scipy import signal
import pyaudio
import audioop
from running_filter import FilterType


##############################################################
#   Variable Definition
##############################################################
CHUNK_SIZE = 1024
STEP_LEVEL = 1.25


##############################################################
#   Class Definition
##############################################################
class AudioAction:
    def __init__(self, track_id_library, file_library, audio=None):
        # Allocated Storage
        self.original = audio  # The Original
        self.audio_original = audio  # Bytes
        self.audio_modified = None  # Bytes
        self.audio_temp = None  # Bytes
        # Pre Determined Libraries
        self.track_id_library = track_id_library
        self.file_library = file_library
        # Class Parameter
        self.already_faded = False
        self.already_equalized = False
        self.already_reversed = False
        self.last_operation = None
        self.last_last_operation = None

    # {Hidden Function} Determine and judge if audio need to be renewed
    # load_audio()
    # Input: Depends
    # Output: None
    def load_audio(self, track_id=None, wave_file=None):
        print("Warning: Loading new audio will over-write all previous unsaved changes")
        # Determine if there is a audio file to play
        if (not track_id) and (not wave_file) and (not self.audio_original):
            print("Error(1003): Unable to determine audio file")
            return
        # Load if only track_id is given but not wave_file
        elif track_id and (not wave_file):
            print("ONLY Track ID Detected from input [USED]")
            if track_id in self.track_id_library.values:
                track_loc = self.track_id_library.loc[self.track_id_library == track_id]
                wave_file = self.file_library.at[track_loc]
            else:
                print(" Track ID not found in the library")
                return
        # Load if wave file is given and both given
        elif wave_file:
            if track_id:
                print(" Track ID is detected in the input [IGNORED]")
            print(" Wave File is detected in the input [USED]")
            wave_file = wave_file
        # All other scenario
        else:
            print("Error(1004): Unable to determine audio")

        # Load wav to audio if wave_file is defined
        if wave_file:
            # Make sure file type is wav
            if not wave_file.lower().endswith(".wav"):
                # Convert File to wav
                try:
                    if os.path.isfile(wave_file):
                        mod_command = "ffmpeg -i " + wave_file + " -acodec pcm_s16le -ar 44100 temp.wav"
                        subprocess.call(mod_command)
                    else:
                        print("Error(1005): No such file in the director")
                        print(" Audio not loaded")
                        return
                except OSError:
                    print("Error(1005): Unable to use ffmpeg")
                    print(" Audio not loaded")
                    return
                # Open and store the wav file to system
                self.audio_original = wave.open("temp.wav", "rb")
                self.audio_modified = self.audio_original
                self.audio_temp = self.audio_original
                # Remove Temp File
                os.remove("temp.wav")
            else:
                self.original = wave.open(wave_file, "rb")
                self.audio_original = self.original.readframes(-1)
                self.audio_modified = self.audio_original
                self.audio_temp = self.audio_original

    # Obtain modified track
    # obtain_modified_track()
    # Input: None
    # Output: audio_modified
    def obtain_modified_track(self):
        return self.audio_modified

    # Apply audio with default process
    # default_process(track_id, equalizer_type)
    # Input: track_id, equalizer_type
    # Output: modified audio
    def default_process(self, track_id, equalizer_type, save=True, file_name="default_processed.wav"):
        # Load audio
        self.load_audio(track_id=track_id)
        # add fade
        self.fade(fade=12, use_original=False)
        # add equalizer
        self.equalizer(equalizer_type=equalizer_type, use_original=False, save=save, file_name=file_name)
        # return modified track
        return self.audio_modified

    # Unapply last modification
    # unapply_last_modification()
    # Input: None
    # Output: None
    def unapply_last_modification(self):
        if not self.audio_temp:
            print("Unsuccessful due to no previous modification detected")
        else:
            # Last Operation
            if self.last_operation == "EQUALIZER":
                self.already_equalized = False
            elif self.last_operation == "REVERSE":
                self.already_reversed = False
            elif self.last_operation == "FADE":
                self.already_faded = False
            # Last Last Operation
            if self.last_last_operation == "REVERSE":
                self.already_reversed = True
            elif self.last_last_operation == "EQUALIZER":
                self.already_equalized = True
            elif self.last_last_operation == "FADE":
                self.already_faded = True
            # Operation
            temp = self.last_operation
            self.last_operation = self.last_last_operation
            self.last_last_operation = temp
            # Track
            temp = self.audio_modified
            self.audio_modified = self.audio_temp
            self.audio_temp = temp

    # Plot the spectrogram or wave form
    # plot(spectogram, save)
    # Input: True/False
    # Output: Depends
    def plot(self, spectrogram=False, use_original=False, save=False):
        # Determine audio file
        if use_original:
            audio = self.audio_original
        else:
            audio = self.audio_modified
        # Whether audio is loaded
        if audio:
            # Plot process
            if not spectrogram:
                # audio_signal = audio.readframes(-1)
                audio_signal = audio
                audio = self.original
                if audio.getsampwidth() == 1:
                    audio_signal = np.array(np.frombuffer(audio_signal, dtype='UInt8') - 128, dtype="Int8")
                elif audio.getsampwidth() == 2:
                    audio_signal = np.frombuffer(audio_signal, dtype='Int16')
                else:
                    raise RuntimeError("Unsupported sample width")
                deinnerleaved = [audio_signal[idx::audio.getnchannels()] for idx in
                                 range(audio.getnchannels())]
                # Get time from indices
                fs = audio.getframerate()
                audio_time = np.linspace(0, len(audio_signal) / audio.getnchannels() / fs,
                                         num=len(audio_signal) / audio.getnchannels())
                plt.figure(figsize=(50, 3))
                # Plot
                plt.figure(1)
                plt.title('Signal Wave')
                for channel in deinnerleaved:
                    plt.plot(audio_time, channel, linewidth=.125)
                plt.xlabel("time [s]")
                plt.ylabel("Amplitude")
                if save:
                    plt.savefig("Signal Wave.png")
                else:
                    plt.show()
            else:
                # Additional information
                print("### This Feature only support unmodified tracks ###")
                # Save audio to temp file with mono
                self.save_audio(file_name="dual_temp", use_original=use_original)
                mod_commend = "ffmpeg -i dual_temp.wav -acodec pcm_s16le -ar 44100 -ac 1 mono_temp.wav"
                try:
                    subprocess.call(mod_commend)
                except OSError:
                    print("Error(1012): Unable to use ffmpeg")
                    os.remove("dual_temp.wav")
                    return
                # Obtain and reload the mono audio file
                fs, audio_data = wavfile.read("mono_temp.wav")
                # Spectrum
                n = len(audio_data)
                audio_frequency = fft(audio_data)
                audio_frequency = audio_frequency[
                                  0:int(np.ceil((n + 1) / 2.0))]  # Select half of the spectrum
                frequency_magnitude = np.abs(audio_frequency)
                frequency_magnitude = frequency_magnitude / float(n)
                # Power Spectrum
                frequency_magnitude = frequency_magnitude ** 2  # Power of Spectrum
                if n % 2 > 0:  # fft odd
                    frequency_magnitude[1:len(frequency_magnitude)] = frequency_magnitude[
                                                                      1:len(frequency_magnitude)] * 2
                else:  # fft even
                    frequency_magnitude[1:len(frequency_magnitude) - 1] = frequency_magnitude[
                                                                          1:len(
                                                                              frequency_magnitude) - 1] * 2
                plt.figure()
                freq_axis = np.arange(0, int(np.ceil((n + 1) / 2.0)), 1.0) * (fs / n)
                plt.plot(freq_axis / 1000.0, 10 * np.log10(frequency_magnitude))  # Power spectrum
                plt.xlabel('Frequency (kHz)')
                plt.ylabel('Power spectrum (dB)')
                # Spectrogram
                nfft = 512  # Number of point in the fft
                f, t, sxx = signal.spectrogram(audio_data, fs, window=signal.windows.blackman(nfft),
                                               nfft=nfft)
                plt.figure()
                plt.pcolormesh(t, f, 10 * np.log10(sxx))  # dB spectrogram
                # plt.pcolormesh(t, f, sxx) # Lineal spectrogram
                plt.ylabel('Frequency [Hz]')
                plt.xlabel('Time [seg]')
                plt.title('Spectrogram', size=16)
                if save:
                    plt.savefig("Spectrogram Diagram.png")
                else:
                    plt.show()
                # Clean up temp file
                os.remove("dual_temp.wav")
                os.remove("mono_temp.wav")
        else:
            print("Error(1013): audio not loaded")

    # Save audio to file from self.audio
    # save_audio()
    # Input: None
    # Output: wav file
    def save_audio(self, file_name="output", extension="wav", use_original=False):
        # Determine save audio type
        if use_original:
            audio = self.audio_original
        else:
            audio = self.audio_modified
        # Whether audio is loaded
        if audio:
            # Save audio to file
            save_name = file_name + "." + "wav"
            wg = wave.open(save_name, "wb")
            param = self.original.getparams()
            wg.setparams(param)
            # Write to file
            wg.writeframes(audio)
            # for chunk in range(0, len(audio), CHUNK_SIZE):
            #     wg.writeframes(audio[chunk:chunk + CHUNK_SIZE])
            # Close file
            wg.close()
            if extension.lower() == "mp3":
                mod_commend = "ffmpeg -i " + save_name + " -acodec pcm_s16le -ar 44100 " + file_name + ".mp3"
                try:
                    subprocess.call(mod_commend)
                    print("File Saved")
                except OSError:
                    print("Error(1014): Unable to use ffmpeg")
            elif extension.lower() == "wav":
                print("File Saved")
        else:
            print("Error(1011): audio not loaded")

    # Play audio to speaker from self.audio
    # play_audio()
    # Input: None
    # Output: Sound in Speaker
    def play_audio(self, use_original=False):
        print("Now Playing Audio...")
        # Determine save audio type
        if use_original:
            signal = self.audio_original
        else:
            signal = self.audio_modified
        # Whether audio is loaded
        if signal:
            # Initialize pyaudio
            p = pyaudio.PyAudio()
            audio = self.original
            # Open Stream
            stream = p.open(format=p.get_format_from_width(audio.getsampwidth()),
                            channels=audio.getnchannels(),
                            rate=audio.getframerate(),
                            output=True)
            # Play Stream
            stream.write(frames=signal, num_frames=None)
            # Stop Stream
            stream.stop_stream()
            stream.close()
            p.terminate()
        else:
            print("Error(1010): audio not loaded")

    # add fade effect to audio
    # fade(fade)
    # Input: fade_seconds
    # Output: None
    def fade(self, fade=12, use_original=False):
        # Determine save audio type
        if use_original:
            signal = self.audio_original
            print("WARNING: Using original will delete unsaved previously modified track")
            # Empty Controller
            self.already_faded = False
            self.already_equalized = False
            self.already_reversed = False
            self.last_operation = None
            self.last_last_operation = None
        else:
            signal = self.audio_modified
        # Whether audio is loaded
        if signal:
            # Determine if already applied fade
            if not self.already_faded:
                # Obtain necessary information from audio
                duration = np.floor(self.original.getnframes() / float(self.original.getframerate()))
                # Read Data
                audio = self.original
                index = 0
                data = signal[index:index + CHUNK_SIZE]
                # Add Fade to stream
                temp = []
                step = 0
                while len(data) > 0:
                    # Calculate Play Time
                    # play_time = np.round(0.0232274 * step - 0.369193)
                    play_time = np.round(0.00579174 * step - 6136/24863)
                    # Fade Process
                    if 0 <= play_time <= fade:
                        data = audioop.mul(data, audio.getsampwidth(), 1 * play_time / fade)
                    elif duration - fade <= play_time <= duration:
                        data = audioop.mul(data, audio.getsampwidth(), 1 * (duration - play_time) / fade)
                    elif fade < play_time < duration - fade:
                        data = audioop.mul(data, audio.getsampwidth(), 1)
                    # Append to temp
                    temp.append(data)
                    index = index + CHUNK_SIZE
                    data = signal[index:index + CHUNK_SIZE]
                    step += 1
                # Save modified track to audio
                signal = b"".join(temp)[:]
                # Assign to class variable
                self.audio_temp = self.audio_modified
                self.audio_modified = signal
                self.already_faded = True
                # Operation
                self.last_last_operation = self.last_operation
                self.last_operation = "FADE"
            else:
                print("No fade applied due to effect already applied")
        else:
            print("Error(1009): audio not loaded")

    # reverse audio
    # reverse_track()
    # Input: None
    # Output: None
    def reverse_track(self, use_original=False):
        # Determine save audio type
        if use_original:
            audio = self.audio_original
            print("WARNING: Using original will delete unsaved previously modified track")
            # Empty Controller
            self.already_faded = False
            self.already_equalized = False
            self.already_reversed = False
            self.last_operation = None
            self.last_last_operation = None
        else:
            audio = self.audio_modified

        if audio:
            # Reverse Track
            if not self.already_reversed:
                full_data = []
                index = 0
                data = audio[index:index + CHUNK_SIZE]
                # Load track
                while data:
                    full_data.append(audioop.mul(data, self.original.getsampwidth(), 0.00375))
                    index = index + CHUNK_SIZE
                    data = audio[index:index + CHUNK_SIZE]
                # Reverse track data
                data = b"".join(full_data)[::-1]
                # Save to class variable
                self.audio_temp = self.audio_modified
                self.audio_modified = data
                # Operation
                self.last_last_operation = self.last_operation
                self.last_operation = "REVERSE"
            else:
                print("Track has already been reversed")
        else:
            print("Error(1008): audio not loaded")

    # Apply equalizer to audio
    # equalizer(equalizer_type)
    # Input: equalizer_type
    # Output: None
    def equalizer(self, equalizer_type, use_original=False, play=False, save=False, file_name="equalized.wav"):
        # Determine save audio type
        if use_original:
            audio = self.audio_original
            print("WARNING: Using original will delete unsaved previously modified track")
            # Empty Controller
            self.already_faded = False
            self.already_equalized = False
            self.already_reversed = False
            self.last_operation = None
            self.last_last_operation = None
        else:
            audio = self.audio_modified
        # Temp Parameter
        audio_mod = None
        # Whether audio is loaded
        if audio:
            print("### Only One Filter can be applied at the time ###")
            # Equalizer Controller
            eq = self.Equalizer(audio_original=self.original, mod_audio=audio)
            # Determine the equalizer and apply to audio
            if equalizer_type.lower() == "acoustic":
                eq.acoustic(save=save, play=play, file_name=file_name)
            elif equalizer_type.lower() == "vocal":
                eq.vocal(save=save, play=play, file_name=file_name)
            elif equalizer_type.lower() == "piano":
                eq.piano(save=save, play=play, file_name=file_name)
            else:
                print("Error(1006): Unknown equalizer")
            # Save to class variable
            if not audio_mod:
                self.audio_temp = self.audio_modified
                self.audio_modified = audio_mod
                # Operation
                self.last_last_operation = self.last_operation
                self.last_operation = "EQUALIZER"
        else:
            print("Error(1007): audio not loaded")

    # Equalizer Class
    class Equalizer:
        def __init__(self, audio_original, mod_audio):
            self.audio = audio_original
            self.mod_audio = mod_audio
            self.filtering = FilterType(audio=self.audio, mod_audio=self.mod_audio)

        # Apply Acoustic Equalizer
        def acoustic(self, save=False, play=False, file_name="acoustic_filtered.wav"):
            print("Applying Acoustic equalizer")
            self.filtering.band_pass_filter(low_frequency=500, high_frequency=1000, save_result=save, play=play, file_name=file_name)

        # Apply Vocal Equalizer
        def vocal(self, save=False, play=False, file_name="vocal_filtered.wav"):
            print("Applying Vocal equalizer")
            self.filtering.band_pass_filter(low_frequency=5000, high_frequency=10000, save_result=save, play=play, file_name=file_name)

        # Apply Piano Equalizer
        def piano(self, save=False, play=False, file_name="piano_filtered.wav"):
            print("Applying Piano equalizer")
            self.filtering.band_pass_filter(low_frequency=250, high_frequency=500, save_result=save, play=play, file_name=file_name)


##############################################################
#   Function Prototype
##############################################################
def test():
    audio_action = AudioAction(track_id_library=1, file_library=1, audio=None)
    audio_action.load_audio(wave_file="clip2.wav")
    # audio_action.plot(spectrogram=False, use_original=True, save=False)
    # audio_action.plot(spectrogram=True, use_original=True, save=False)
    audio_action.fade(fade=12, use_original=True)
    # audio_action.reverse_track(use_original=False)
    # audio_action.save_audio(file_name="temp", extension="wav", use_original=False)
    # audio_action.play_audio(use_original=False)
    audio_action.equalizer(equalizer_type="vocal", use_original=False, save=True, play=True, file_name="vocal_equalized.wav")


    print("Here")


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

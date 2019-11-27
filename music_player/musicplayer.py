# Music Player Project
# Version: 2.3.1
# V2.4.x -> Import Equalizer Class
# V2.5.x -> Import Dynamic Programming for character mismatch search

##############################################################
#   Libraries
##############################################################
import numpy as np
import random
import pandas as pd
import pyaudio
import wave
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile
from scipy import signal
import audioop
import os
import threading as td
import subprocess
import math
import pydub


##############################################################
#   Variable Definition
##############################################################
CHUNK_SIZE = 1024
STEP_LEVEL = 1.25


##############################################################
#   Class Prototype
##############################################################
# Library Class
# Create a playlist from save music library
# API Operation                                         | Description
# Library(length, [file], [repeat])                     | Create a playlist with music library file
# print(playlist)                                       | Print current playlist
# delete_track(playlist, delete_track_location)         | Delete a track in the specific location of the playlist
# add_track(playlist, add_track_id, add_track_location) | Add a track to a specific location of the playlist
# search(targets)                                       | Search library for track id, artist, or track name matches
#                                                         selected target input
# audio_action.load_audio(track_id)                     | Load specific track for audio action
# audio_action.unapply_last_modification()              | Undo the last modification done on the audio
# audio_action.save_audio([use_original])               | Save audio to file
# audio_action.play_audio([use_original])               | Play audio
# audio_action.fade([fade], [use_original])             | Apply fade to audio
# audio_action.reverse_track([use_original])            | Reverse audio
# audio_action.equalizer(equalizer_type, [use_original])| Apply equalizer effect to audio
# audio_action.plot([spectrogram], [use_original])      | Plot the wave form or pectrogram of selected audio
# playlist_to_audio(playlist, equalizer_type, file_name, extension)
#                                                       | Covert the whole playlist to a big file with equalizer effect
class Library:
    def __init__(self, length, file_name="raw_track_short.csv", repeat=False):
        # Check if file exists
        if not os.path.isfile(file_name):
            print("Error(1001): Unable to locate the file")
            exit(1001)
        # Read in the file
        self.data = pd.read_csv(filepath_or_buffer=file_name)
        # Reload to library sub information
        self.track_id = self.data["track_id"]
        self.track_id_np = np.asarray(self.track_id)
        self.track_name = self.data["track_title"]
        self.artist = self.data["artist_name"]
        self.album = self.data["album_title"]
        self.file_location = self.data["track_file"]
        # Generate library label
        self.lib_index = [loop0 for loop0 in range(0, self.data.shape[0])]
        self.lib_column = ["track_id", "track_title", "artist_name", "album_title", "track_file"]
        # Recreate library
        lib_data = np.column_stack((self.track_id, self.track_name, self.artist, self.album, self.file_location))
        self.library = pd.DataFrame(lib_data, index=self.lib_index, columns=self.lib_column)
        self.info_num = self.library.shape[1]
        # Check if length is longer than file size
        data_range = self.data.shape[0]
        if length > data_range:
            print("## Length Out of Range ##")
            self.length = data_range
        else:
            self.length = length
        # Generate a random list
        random_list = np.zeros(self.length)
        index = 0
        while index <= length - 1:
            temp_num = random.randint(0, data_range - 1)
            # Check if exists
            if not repeat:
                exist = 0
                for index2 in range(0, self.length):
                    if temp_num == int(random_list[index2]):
                        exist = 1
                if exist == 0:
                    random_list[index] = temp_num
                    index += 1
                else:
                    index = index
            else:
                random_list[index] = temp_num
                index += 1
        # Obtain Playlist
        self.playlist = random_list.reshape((self.length, 1))
        # Temp Storage for Values
        self.artist_search_result = None
        self.track_name_search_result = None
        self.audio = None
        self.audio_id = None
        self.mega_audio = None
        # Sub Class Action
        self.audio_action = self.AudioAction(track_id_library=self.track_id, file_library=self.file_location)

    # Return the original playlist
    # str
    # Input: None
    # Output: None
    def __str__(self):
        return [self.library.at[item] for item in self.playlist]

    # Print the current playlist
    # print(playlist)
    # Input: playlist
    # Output: None
    def print(self, playlist):
        print([self.library.at[item] for item in playlist])

    # Delete a track from the playlist
    # detele_track(playlist, delete_track_location)
    # Input: playlist, delete_track_location
    # Output: modified playlist
    def delete_track(self, playlist, delete_track_location):
        # Check delete index out of range
        outer_range = playlist.shape[0]
        if delete_track_location > outer_range or delete_track_location < 1:
            print("*** Error(1002): Delete Out of Index ***")
        else:
            print("Item has been deleted from Playlist")
            temp = np.delete(playlist, delete_track_location - 1, axis=0)
            self.print(playlist=temp)
            return temp

    # Add a track to the playlist
    # add_track(playlist, add_track_id, add_track_location)
    # Input: playlist, add_track_id, add_track_location
    # Output: modified playlist
    def add_track(self, playlist, add_track_id, add_track_location):
        outer_range = playlist.shape[0]
        # Find the corresponding track info
        if add_track_id in self.track_id.values:
            track_loc = int(self.track_id.loc[self.track_id.values == add_track_id].values)
            # Check add index out of range
            if add_track_location > outer_range or add_track_location < 1:
                print("### Add Out of Index ###")
                add_loc = playlist.shape[0]
            else:
                add_loc = add_track_location - 1
            # Add to playlist
            print("Item has been added to Playlist")
            temp = np.insert(playlist, add_loc, track_loc, axis=0)
            self.print(playlist=temp)
            return temp
        else:
            print("*** Selected track Not found in the library ***")

    # search the library for targets
    # search(targets)
    # Input: target
    # Output: Terminal Print
    def search(self, targets):
        # Sub functions for search
        # {Hidden Function} Search by Track Name
        # search_track_name(search_name)
        # Input: search_name
        # Output: print out search result
        def search_track_name(search_name, match=True):
            print("Searching library with track name of", search_name)
            if match:
                if search_name in self.track_name.values:
                    self.track_name_search_result = self.track_id.loc[self.track_name == search_name]
            else:
                print("Under Construction")
            # TODO: Add Approximate Match with Dynamic Programming

        # {Hidden Function} Search by Artist
        # search_track_name(search_artist)
        # Input: search_artist
        # Output: print out search result
        def search_artist(search_artist, match=True):
            print("Searching library with artist name of", search_artist)
            if match:
                if search_artist in self.artist.values:
                    self.artist_search_result = self.track_id.loc[self.artist == search_artist]
            else:
                print("Under Construction")
            # TODO: Add Approximate Match with Dynamic Programming

        # Search function
        targets = targets.strip()
        # Search via Track ID
        if targets.isNumeric():
            print("Searching library with track name of", targets)
            if targets in self.track_name.values:
                track_loc = self.track_id.loc[self.track_name == targets]
                print(self.library.at[track_loc])
            else:
                print(" Track Name not found in the library")
        else:
            # Setup for search in track name and artist For EXACT MATCH
            threads = []
            thread1 = td.Thread(target=search_artist(search_artist=targets))
            thread2 = td.Thread(target=search_track_name(search_name=targets))
            # Start Searching
            thread1.start()
            threads.append(thread1)
            thread2.start()
            threads.append(thread2)
            # Wait till finish
            for t in threads:
                t.join()
            # Print Result for artist search
            if not self.artist_search_result:
                print([self.library.at[item] for item in self.artist_search_result])
            else:
                print(" Artist not found in the library")
            # TODO: Add Approximate Match with Dynamic Programming
            # Print Result for track name search
            if not self.track_name_search_result:
                print([self.library.at[item] for item in self.track_name_search_result])
            else:
                print(" Track Name not found in the library")

    # Covert all songs in a playlist to a wav file
    # playlist_to_audio(playlist, equalizer_type)
    # Input: playlist, equalizer_type
    # Output: local audio file
    def playlist_to_audio(self, playlist, equalizer_type, file_name, extension):
        self.mega_audio = []
        # Process equalizer_type length
        equalizer = equalizer_type * np.ceil(playlist.shape[0] / len(equalizer_type))
        # loop through playlist for individual songs
        for index in range(0, playlist.shape[0]):
            self.mega_audio.append(self.audio_action.default_process(track_id=playlist[index],
                                                                     equalizer_type=equalizer[index]))
        # Save the mega file
        self.AudioAction(track_id_library=self.track_id,
                         file_library=self.file_location,
                         audio=self.mega_audio).save_audio(file_name=file_name,
                                                           extension=extension,
                                                           use_original=True)

    # Sub Class Audio Action
    class AudioAction:
        def __init__(self, track_id_library, file_library, audio=None):
            # Allocated Storage
            self.original = audio  # The Original
            self.audio_original = audio.readframes(-1)  # Bytes
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

            # Load wav to audio if wave_file si defined
            if not wave_file:
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
                    self.audio_original = wave.open(wave_file, "rb")
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
        # TODO: FIX THIS
        def default_process(self, track_id, equalizer_type):
            # Load audio
            self.load_audio(track_id=track_id)
            # add fade
            self.fade(fade=12, use_original=False)
            # add equalizer
            self.equalizer(equalizer_type=equalizer_type, use_original=False)
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
            if not audio:
                # Plot process
                if not spectrogram:
                    # audio_signal = audio.readframes(-1)
                    audio_signal = audio
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
                    if save:
                        plt.savefig("Signal Wave.png")
                    else:
                        plt.show()
                else:
                    # Additional information
                    print("### This Feature only support unmodified tracks ###")
                    # Save audio to temp file with mono
                    self.save_audio(file_name="dual_temp.wav", use_original=use_original)
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
            if not audio:
                # Save audio to file
                save_name = file_name + "." + "wav"
                wg = wave.open(save_name, "wb")
                param = self.original.getparams()
                wg.setparams(param)
                # Write to file
                for chunk in range(0, len(audio), CHUNK_SIZE):
                    wg.writeframes(audio[chunk:chunk + CHUNK_SIZE])
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
            # Determine save audio type
            if use_original:
                audio = self.audio_original
            else:
                audio = self.audio_modified
            # Whether audio is loaded
            if not audio:
                # Initialize pyaudio
                p = pyaudio.PyAudio()
                # Open Stream
                stream = p.open(format=p.get_format_from_width(audio.getsampwidth()),
                                channels=audio.getnchannels(),
                                rate=audio.getframerate(),
                                output=True)
                # Read Data
                data = audio.readframes(CHUNK_SIZE)
                # Play Stream
                while len(data) > 0:
                    data = audioop.mul(data, audio.getsampwidth(), STEP_LEVEL)
                    stream.write(frames=data, num_frames=None)
                    data = audio.readframes(CHUNK_SIZE)
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
            # Whether audio is loaded
            if not audio:
                # Determine if already applied fade
                if not self.already_faded:
                    # Obtain necessary information from audio
                    duration = np.floor(audio.getnframes() / float(audio.getframerate()))
                    # Read Data
                    data = audio.readframes(CHUNK_SIZE)
                    # Add Fade to stream
                    temp = []
                    step = 0
                    while len(data) > 0:
                        # Calculate Play Time
                        play_time = np.round(0.0232274 * step - 0.369193)
                        # Fade Process
                        if 0 <= play_time <= fade:
                            data = audioop.mul(data, audio.getsampwidth(), 1 * play_time / fade)
                        elif duration - fade <= play_time <= duration:
                            data = audioop.mul(data, audio.getsampwidth(), 1 * (duration - play_time) / fade)
                        else:
                            data = audioop.mul(data, audio.getsampwidth(), 1)
                        # Append to temp
                        temp.append(data)
                        data = audio.readframes(CHUNK_SIZE)
                    # Save modified track to audio
                    audio = b"".join(temp)[:]
                    # Assign to class variable
                    self.audio_temp = self.audio_modified
                    self.audio_modified = audio
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

            if not audio:
                # Reverse Track
                if not self.already_reversed:
                    full_data = []
                    data = audio.readframes(CHUNK_SIZE)
                    # Load track
                    while data:
                        full_data.append(audioop.mul(data, audio.getsampwidth(), 0.00375))
                        data = audio.readframes(CHUNK_SIZE)
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
        def equalizer(self, equalizer_type, use_original=False):
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
            if not audio:
                # Equalizer Controller
                eq = self.Equalizer(audio=audio)
                # Determine the equalizer and apply to audio
                if equalizer_type.lower() == "acoustic":
                    audio_mod = eq.acoustic()
                elif equalizer_type.lower() == "late night":
                    audio_mod = eq.late_night()
                elif equalizer_type.lower() == "pop":
                    audio_mod = eq.pop()
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
            def __init__(self, audio):
                self.audio = audio

                # TODO: Add specific process towards equalizer process

            def acoustic(self):
                print("Applying Acoustic equalizer")
                modified_audio = self.audio
                return modified_audio

            def late_night(self):
                print("Applying Late Night equalizer")
                modified_audio = self.audio
                return modified_audio

            def pop(self):
                print("Applying Pop equalizer")
                modified_audio = self.audio
                return modified_audio


##############################################################
#   Function Prototype
##############################################################
def test_api():
    print("Testing API")
    # Generate a random playlist of n songs
    playlist_length = 8
    # Load library from file and playlist does not contain repeat item
    lib = Library(length=playlist_length, file_name="raw_track_short.csv", repeat=False)
    playlist = lib.playlist
    print(lib.print(playlist=playlist))
    print("*****************************************************")
    # Delete a track from the generated playlist
    delete_track_location = 3
    playlist = lib.delete_track(playlist=playlist, delete_track_location=delete_track_location)
    print("*****************************************************")
    # Add a song to the existing playlist
    add_track_id = 142
    add_track_location = 2
    playlist = lib.add_track(playlist=playlist, add_track_id=add_track_id, add_track_location=add_track_location)
    print("*****************************************************")
    # Search for track id in library
    search_id = 20
    lib.search(targets=search_id)
    print("*****************************************************")
    # Search for artist in library
    search_artist = "AWOL"
    lib.search(targets=search_artist)
    print("*****************************************************")
    # Search for track name in library
    search_track = "Yosemite"
    lib.search(targets=search_track)
    print("*****************************************************")
    # Audio Manipulation
    target_track_id = 135
    lib.audio_action.load_audio(track_id=target_track_id)
    # Reverse track
    lib.audio_action.reverse_track(use_original=True)  # To modify using original track
    # Apply Filter
    lib.audio_action.equalizer(equalizer_type="Acoustic", use_original=False)
    # Undo last modification and reapply a different filter
    lib.audio_action.unapply_last_modification()
    lib.audio_action.equalizer(equalizer_type="Late Night", use_original=False)
    print("*****************************************************")
    # Save modified track as temp_name.wav
    lib.audio_action.save_audio(file_name="temp_name", extension="wav", use_original=False)
    # Save original track as org_name.mp3
    lib.audio_action.save_audio(file_name="org_name", extension="mp3", use_original=True)
    print("*****************************************************")
    # Plot wave form of the original audio and save
    lib.audio_action.plot(spectrogram=False, use_original=True, save=True)
    # Plot wave form of the modified audio and save
    lib.audio_action.plot(spectrogram=False, use_original=False, save=True)
    # Plot spectrogram of the original audio and save
    lib.audio_action.plot(spectrogram=True, use_original=True, save=True)
    print("*****************************************************")
    # Batch adjust all songs in playlist with only acoustic type and output as one big file
    equalizer = ["Acoustic"]
    lib.playlist_to_audio(playlist=playlist, equalizer_type=equalizer, file_name="mega_playlist", extension="wav")
    # Batch adjust all songs in playlist with equalizer in the following order and output as one big file
    equalizer = ["Acoustic", "Pop", "Piano"]
    lib.playlist_to_audio(playlist=playlist, equalizer_type=equalizer, file_name="mega_playlist", extension="wav")


##############################################################
#   Main Function
##############################################################
def running_mean(x, windowSize):
  cumsum = np.cumsum(np.insert(x, 0, 0))
  return (cumsum[windowSize:] - cumsum[:-windowSize]) / windowSize

def interpret_wav(raw_bytes, n_frames, n_channels, sample_width, interleaved = True):

    if sample_width == 1:
        dtype = np.uint8 # unsigned char
    elif sample_width == 2:
        dtype = np.int16 # signed 2-byte short
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


def main():
    print("Hello World!")
    sampleRate = 44100
    cutOffFrequency = 400.00
    freqRatio = (cutOffFrequency / sampleRate)

    N = int(math.sqrt(0.196196 + freqRatio ** 2) / freqRatio)
    print("Here")


##############################################################
#    Main Function Runner
##############################################################
if __name__ == "__main__":
    try:
        main()
    except:
        print("Error")

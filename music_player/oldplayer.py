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
import datetime
import audioop

##############################################################
#   Variable Definition
##############################################################
CHUNK_SIZE = 1024
STEP_LEVEL = 1.25


##############################################################
#   Class Definition
##############################################################
# Node Class
# Create a Node and its data
# API Operation                     | Description
# Node(track_id)                    | Create Node
# str                               | Print track_id
class Node:
    # Initialize a node
    # Node(track_id)
    # Input: track_id
    # Output: None
    def __init__(self, track_id, track_name=None, artist=None, album=None, file_location=None, next=None):
        self.track_id = track_id
        self.track_name = track_name
        self.artist = artist
        self.album = album
        self.file_location = file_location
        self.next = next

    # Print track_id
    # str()
    # input: None
    # Output: string of track_id
    def __str__(self):
        return str(self.track_id)


# LinkedList class
# Create a linked list
# API Operation                     | Description
# LinkedList(head)                  | Create a LinkedList by initialize the head
# len                               | Print the length of the LinkedList
# insert_to_front(data)             | Create a data Node and set to the head
# find(data)                        | Find Node with desired data
# append(data)                      | Append new data to the end
# delete(data)                      | Delete Node with desired data
# insert_after(pre_data, data)      | Insert a data Node right after the current one
# print_list()                      | Print the whole LinkedList
class LinkedList(object):
    # Initialize a LinkedList
    # LinkedList(data)
    # Input: data
    # Output: None
    def __init__(self, head):
        self.head = head

    # print LinkedList length
    # len()
    # Input: None
    # Output: length of the LinkedList
    def __len__(self):
        current = self.head
        counter = 0
        while current is not None:
            counter += 1
            current = current.next
        return counter

    # Find the nth linked Node
    # find_nth(n)
    # Input: n as integer
    # Output nth's track_id
    def find_nth(self, n):
        current = self.head
        counter = 0
        track_id = 0
        if n <= 0:
            print("Invalid Input in Finding Location")
            exit(1)
        while counter < n:
            counter += 1
            current = current.next
            track_id = current.track_id
            if current.next is None:
                print("Not Found in the List")
                return track_id
        return track_id

    # insert to the front
    # insert_to_front(data)
    # Input: data
    # Output: newly created node
    def insert_to_front(self, track_id, track_name=None, artist=None, album=None, file_location=None):
        if track_id is None:
            return None
        node = Node(track_id=track_id, track_name=track_name, artist=artist, album=album, file_location=file_location,
                    next=self.head)
        self.head = node
        return node

    # Find Node with desired track_id
    # find(track_id)
    # Input: track_id
    # Output: None
    def find(self, track_id, feedback=False):
        if track_id is None:
            return None
        curr_node = self.head
        while curr_node is not None:
            if curr_node.track_id == track_id:
                return curr_node
            curr_node = curr_node.next
        # Determine Feedback
        if feedback:
            return curr_node
        else:
            return None

    # Append new data to the end
    # append(data)
    # Input: data
    # Output: None
    def append(self, track_id, track_name=None, artist=None, album=None, file_location=None):
        if track_id is None:
            return None
        node = Node(track_id=track_id, track_name=track_name, artist=artist, album=album, file_location=file_location)
        if self.head is None:
            self.head = node
            return node
        curr_node = self.head
        while curr_node.next is not None:
            curr_node = curr_node.next
        curr_node.next = node
        return node

    # Delete Node if data matches
    # delete(data)
    # Input: data
    # Output: None
    def delete(self, track_id):
        if track_id is None:
            return None
        if self.head is None:
            return None
        if self.head.track_id == track_id:
            self.head = self.head.next
            return
        prev_node = self.head
        curr_node = self.head.next
        while curr_node is not None:
            if curr_node.track_id == track_id:
                prev_node.next = curr_node.next
                return
            else:
                prev_node = curr_node
                curr_node = curr_node.next

    # Insert after certain node
    # insert_after(pre_data, data)
    # Input: pre_data, data
    # Output: None
    def insert_after(self, pre_track_id, track_id, track_name=None, artist=None, album=None, file_location=None):
        new_node = Node(track_id=track_id, track_name=track_name, artist=artist, album=album,
                        file_location=file_location)
        pre_node = self.find(pre_track_id, feedback=True)
        new_node.next = pre_node.next
        pre_node.next = new_node

    # Print the LinkedList
    # print_list()
    # Input: None
    # Output: None
    def print_list(self):
        temp = self.head
        counter = 1
        while temp:
            print(counter, "||", temp.track_id, "|", temp.track_name, "| by:", temp.artist, "| in:", temp.album)
            temp = temp.next
            counter += 1

    # Return shape
    # shape()
    # Input: None
    # Output: [length, height]
    def shape(self):
        return np.asarray([self.__len__(), 5])


# Playlist Class
# Create a playlist from save music library
# API Operation                     | Description
# Playlist(file)                    | Create a playlist with music library file
# random_list(num)                  | Create a playlist of random tracks
# delete_track(track_num)           | Delete a song from the playlist
# add_track(track_num, location)    | Add a song at any location in the playlist
# str                               | Print out playlist with artist name and track and playlist location
# search_track_id(search_id)        | Search library by track id
# search_track_name(search_name)    | Search library by track name
# search_artist(search_artist)      | Search library by artist
# reverse_track(track_id)           | Reverse track
# equalizer(self, track_id)         | Create an equalizer of a track
# plot_spectrogram(self, track_id)  | Plot the spectrogram of a track
# play_audio(track_id)              | Play audio
class Library:
    # Initialize the library
    # Input: length, (file_name, repeat)
    # Output: None
    def __init__(self, length, file_name="raw_tracks.csv", repeat=False, linked_list=False):
        # Set parameter
        self.linked_list = linked_list
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
        # Generate the playlist via LinkedList or Numpy
        if linked_list:
            self.playlist = LinkedList(None)
            for item in random_list:
                track_loc = int(item)
                self.playlist.append(track_id=self.track_id.at[track_loc],
                                     track_name=self.track_name.at[track_loc],
                                     artist=self.artist.at[track_loc],
                                     album=self.album.at[track_loc],
                                     file_location=self.file_location.at[track_loc])
        else:
            self.playlist = random_list.reshape((self.length, 1))

    # Return the original playlist
    # str
    # Input: None
    # Output: None
    def __str__(self):
        if not self.linked_list:
            return [self.library.at[item] for item in self.playlist]
        else:
            return str("Please use LinkedList Print")

    # Print the current playlist
    # print(playlist)
    # Input: playlist
    # Output: None
    def print(self, playlist):
        if not self.linked_list:
            print([self.library.at[item] for item in playlist])
        else:
            playlist.print_list()

    # Delete a track from the playlist
    # detele_track(playlist, delete_track_location)
    # Input: playlist, delete_track_location
    # Output: modified playlist
    def delete_track(self, playlist, delete_track_location):
        # Check delete index out of range
        if self.linked_list:
            outer_range = playlist.__len__()
        else:
            outer_range = playlist.shape[0]
        if delete_track_location > outer_range or delete_track_location < 1:
            print("*** Error: Delete Out of Index ***")
        else:
            print("Item has been deleted from Playlist")
            if self.linked_list:
                track_id = playlist.find_nth(n=delete_track_location - 1)
                playlist.delete(track_id=track_id)
                playlist.print_list()
                new_playlist = LinkedList(head=playlist.head)
                return new_playlist
            else:
                temp = np.delete(playlist, delete_track_location - 1, axis=0)
                self.print(playlist=temp)
                return temp

    # Add a track to the playlist
    # add_track(playlist, add_track_id, add_track_location)
    # Input: playlist, add_track_id, add_track_location
    # Output: modified playlist
    def add_track(self, playlist, add_track_id, add_track_location):
        if self.linked_list:
            outer_range = playlist.__len__()
        else:
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
            if self.linked_list:
                pre_track = playlist.find_nth(n=add_loc)
                playlist.insert_after(pre_track_id=pre_track,
                                      track_id=add_track_id,
                                      track_name=str(self.track_name.loc[self.track_id.values == add_track_id].values),
                                      artist=str(self.artist.loc[self.track_id.values == add_track_id].values),
                                      album=str(self.album.loc[self.track_id.values == add_track_id].values),
                                      file_location=str(
                                          self.file_location.loc[self.track_id.values == add_track_id].values))
                playlist.print_list()
                new_playlist = LinkedList(head=playlist.head)
                return new_playlist
            else:
                temp = np.insert(playlist, add_loc, track_loc, axis=0)
                self.print(playlist=temp)
            return temp
        else:
            print("*** Selected track Not found in the library ***")

    # Search by track id
    # search_track_id(search_id)
    # Input: search_id
    # Output: print out search result
    def search_track_id(self, search_id):
        print("Searching library with track id of", search_id)
        if search_id in self.track_id.values:
            track_loc = self.track_id.loc[self.track_id == search_id]
            print(self.library.at[track_loc])
        else:
            print(" Track ID not found in the library")

    # Search by Track Name
    # search_track_name(search_name)
    # Input: search_name
    # Output: print out search result
    def search_track_name(self, search_name):
        print("Searching library with track name of", search_name)
        if search_name in self.track_name.values:
            track_loc = self.track_id.loc[self.track_name == search_name]
            print(self.library.at[track_loc])
        else:
            print(" Track Name not found in the library")

    # Search by Artist
    # search_track_name(search_artist)
    # Input: search_artist
    # Output: print out search result
    def search_artist(self, search_artist):
        print("Searching library with artist name of", search_artist)
        if search_artist in self.artist.values:
            track_loc = self.track_id.loc[self.artist == search_artist]
            print([self.library.at[item] for item in track_loc])
        else:
            print(" Artist not found in the library")

    # Play audio
    # play_audio(track_id)
    # Input: track_id
    # Output: stream of audio via Speaker
    def play_audio(self, track_id, wave_file=None, fade=12):
        if track_id is None and wave_file is None:
            wave_file = "Close_To_Me_Solo.wav"
        elif track_id is None and wave_file is not None:
            wave_file = wave_file
        else:
            if track_id in self.track_id.values:
                track_loc = self.track_id.loc[self.track_id == track_id]
                wave_file = self.file_location.at[track_loc]
            else:
                print(" Track ID not found in the library")

        if wave_file is not None:
            print("Now Playing ->", wave_file)
            # Open File
            wf = wave.open(wave_file, 'rb')
            duration = np.floor(wf.getnframes() / float(wf.getframerate()))
            # Initialize pyaudio
            p = pyaudio.PyAudio()
            # Open Stream
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)
            # Read Data
            data = wf.readframes(CHUNK_SIZE)
            # Play Stream
            current_second = datetime.datetime.now().second
            counter = 0
            while len(data) > 0:
                # Set Counter
                if current_second != datetime.datetime.now().second:
                    current_second = datetime.datetime.now().second
                    counter += 1

                # Fade Process
                if 0 <= counter <= fade:
                    data = audioop.mul(data, wf.getsampwidth(), STEP_LEVEL * counter / fade)
                elif duration - fade <= counter <= duration:
                    data = audioop.mul(data, wf.getsampwidth(), STEP_LEVEL * (duration - counter) / fade)
                else:
                    data = audioop.mul(data, wf.getsampwidth(), STEP_LEVEL)

                # Streaming
                stream.write(frames=data, num_frames=None)
                data = wf.readframes(CHUNK_SIZE)
            # Close all
            stream.stop_stream()
            stream.close()
            p.terminate()
            wf.close()

    # reverse and play track
    # reverse_track(track_id)
    # Input: track_id
    # Output: stream of audio via Speaker
    def reverse_track(self, track_id, wave_file=None, play=True):
        print("Generating the reversed track")
        # Determine whether a track is found or run sample file
        if track_id is None and wave_file is None:
            wave_file = "Close_To_Me_Solo.wav"
        elif track_id is None and wave_file is not None:
            wave_file = wave_file
        else:
            if track_id in self.track_id.values:
                track_loc = self.track_id.loc[self.track_id == track_id]
                wave_file = self.file_location.at[track_loc]
            else:
                print(" Track ID not found in the library")

        # Reverse Track
        if wave_file is not None:
            wf = wave.open(wave_file, 'rb')
            wg = wave.open("reversed_track.wav", "wb")
            wg.setparams(wf.getparams())

            # Load everything
            full_data = []
            data = wf.readframes(CHUNK_SIZE)
            while data:
                full_data.append(audioop.mul(data, wf.getsampwidth(), 0.00375))
                data = wf.readframes(CHUNK_SIZE)
            # Reverse data
            data = b"".join(full_data)[::-1]
            # Write data
            for i in range(0, len(data), CHUNK_SIZE):
                wg.writeframes(data[i:i + CHUNK_SIZE])
            # close file
            wf.close()
            wg.close()

            if play:
                # Reload Data
                wg = wave.open("reversed_track.wav", "rb")
                p = pyaudio.PyAudio()
                stream = p.open(format=p.get_format_from_width(wg.getsampwidth()),
                                channels=wg.getnchannels(),
                                rate=wg.getframerate(),
                                output=True)
                data = wg.readframes(CHUNK_SIZE)
                print("Now Playing ->", wave_file, "[reversed]")
                for i in range(0, len(data)):
                    data = audioop.mul(data, wg.getsampwidth(), STEP_LEVEL)
                    stream.write(frames=data, num_frames=None)
                    data = wg.readframes(CHUNK_SIZE)
                # Stop stream
                stream.stop_stream()
                stream.close()
                p.terminate()
                wg.close()

    # Show the Spectrogram of the audio track
    # plot_spectrogram(track_id)
    # Input: track_id
    # Output: None
    def plot_spectrogram(self, track_id, wave_file=None, show=True, save=False, wave_plot=False):
        print("This should plot the spectrogram of a track")
        if track_id is None and wave_file is None:
            wave_file = "Cornelia_Street_mono.wav"
        elif track_id is None and wave_file is not None:
            wave_file = wave_file
        else:
            if track_id in self.track_id.values:
                track_loc = self.track_id.loc[self.track_id == track_id]
                wave_file = self.file_location.at[track_loc]
            else:
                print(" Track ID not found in the library")

        if wave_file is not None:
            if wave_plot:
                wav_file = wave.open(wave_file, 'r')

                # Extract Raw Audio from Wav File
                audio_signal = wav_file.readframes(-1)
                if wav_file.getsampwidth() == 1:
                    audio_signal = np.array(np.frombuffer(audio_signal, dtype='UInt8') - 128, dtype='Int8')
                elif wav_file.getsampwidth() == 2:
                    audio_signal = np.frombuffer(audio_signal, dtype='Int16')
                else:
                    raise RuntimeError("Unsupported sample width")

                de_inter_leaved = [audio_signal[idx::wav_file.getnchannels()] for idx in range(wav_file.getnchannels())]

                # Get time from indices
                fs = wav_file.getframerate()
                audio_time = np.linspace(0, len(audio_signal) / wav_file.getnchannels() / fs,
                                         num=len(audio_signal) / wav_file.getnchannels())
                plt.figure(figsize=(50, 3))
                # Plot
                plt.figure(1)
                plt.title('Signal Wave')
                for channel in de_inter_leaved:
                    plt.plot(audio_time, channel, linewidth=.125)
                plt.xlabel("time [s]")
                plt.ylabel("Amplitude")
                if show:
                    plt.show()
                if save:
                    plt.savefig("Signal Wave.png")
                wav_file.close()
            else:
                # Check if mono file
                wf = wave.open(wave_file, "rb")
                if wf.getnchannels() == 1:
                    wf.close()
                    # Read File
                    fs, audio_data = wavfile.read(wave_file)
                    # Spectrum
                    n = len(audio_data)
                    audio_frequency = fft(audio_data)
                    audio_frequency = audio_frequency[0:int(np.ceil((n + 1) / 2.0))]  # Select half of the spectrum
                    frequency_magnitude = np.abs(audio_frequency)
                    frequency_magnitude = frequency_magnitude / float(n)
                    # Power Spectrum
                    frequency_magnitude = frequency_magnitude ** 2  # Power of Spectrum
                    if n % 2 > 0:  # fft odd
                        frequency_magnitude[1:len(frequency_magnitude)] = frequency_magnitude[
                                                                          1:len(frequency_magnitude)] * 2
                    else:  # fft even
                        frequency_magnitude[1:len(frequency_magnitude) - 1] = frequency_magnitude[
                                                                              1:len(frequency_magnitude) - 1] * 2
                    plt.figure()
                    freq_axis = np.arange(0, int(np.ceil((n + 1) / 2.0)), 1.0) * (fs / n)
                    plt.plot(freq_axis / 1000.0, 10 * np.log10(frequency_magnitude))  # Power spectrum
                    plt.xlabel('Frequency (kHz)')
                    plt.ylabel('Power spectrum (dB)')
                    # Spectrogram
                    nfft = 512  # Number of point in the fft
                    f, t, Sxx = signal.spectrogram(audio_data, fs, window=signal.windows.blackman(nfft), nfft=nfft)
                    plt.figure()
                    plt.pcolormesh(t, f, 10 * np.log10(Sxx))  # dB spectrogram
                    # plt.pcolormesh(t, f, sxx) # Lineal spectrogram
                    plt.ylabel('Frequency [Hz]')
                    plt.xlabel('Time [seg]')
                    plt.title('Spectrogram', size=16)
                    if show:
                        plt.show()
                    if save:
                        plt.savefig("Spectrogram Diagram.png")
                else:
                    print("### Error in file type ###")
                    print("Please use a Mono Wav file")

    def equalizer(self, track_id):
        print("This should adjust equalizer of a track")


##############################################################
#   Function Prototype
##############################################################
def test_api():
    # Generate a random playlist of n songs
    random_track_amount = 8
    lib = Library(length=random_track_amount, file_name="raw_track_short.csv", linked_list=False)
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
    # Print current playlist
    # print("Now Printing Over All")
    # print(lib.print(playlist=playlist))
    print("*****************************************************")
    # Play with Sound
    music = "clip1"
    play_file = music + ".wav"
    plot_file = music + "_mono.wav"
    lib.play_audio(track_id=None, wave_file=play_file)
    print("*****************************************************")
    # Invert audio
    lib.reverse_track(track_id=None, wave_file=play_file)
    print("*****************************************************")
    # Generate spectrogram plot
    lib.plot_spectrogram(track_id=None, wave_file=plot_file)


##############################################################
#   Main Function
##############################################################
def main():
    print("Hello World!")
    test_api()


##############################################################
#    Main Function Runner
##############################################################
if __name__ == "__main__":
    main()

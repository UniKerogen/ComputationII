# Music Player Project
# Version: 3.4.3
# V3.5.x -> Import Dynamic Programming for character mismatch search

##############################################################
#   Libraries
##############################################################
import os
import pandas as pd
import numpy as np
import random
import threading as td
from audio_action import AudioAction

##############################################################
#   Variable Definition
##############################################################


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
        self.audio_action = AudioAction(track_id_library=self.track_id, file_library=self.file_location)

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
    def print(self, playlist, list_print=True):
        index = 1
        for item in playlist:
            # print(self.library.loc[item, :].values)
            if list_print:
                print("  List Location: ", index)
                index += 1
                print("  Track ID:    ", self.track_id.iloc[item].values)
                print("  Track Name:  ", self.track_name.iloc[item].values)
                print("  Artist Name: ", self.artist.iloc[item].values)
                print("  Album Name:  ", self.album.iloc[item].values)
            else:
                print("  Track ID:    ", self.track_id.iloc[item])
                print("  Track Name:  ", self.track_name.iloc[item])
                print("  Artist Name: ", self.artist.iloc[item])
                print("  Album Name:  ", self.album.iloc[item])
            print("")

    # Delete a track from the playlist
    # delete_track(playlist, delete_track_location)
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
            track_loc = int(self.track_id.index[self.track_id.values == add_track_id].values)
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
            print("Searching library with track name of [", search_name, "]")
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
            print("Searching library with artist name of [", search_artist, "]")
            if match:
                if search_artist in self.artist.values:
                    self.artist_search_result = self.track_id.loc[self.artist == search_artist]
            else:
                print("Under Construction")
            # TODO: Add Approximate Match with Dynamic Programming

        # Search function
        targets = targets.strip()
        self.track_name_search_result = None
        self.artist_search_result = None
        # Search via Track ID
        if targets.isdigit():
            print("Searching library with track name of [", targets, "]")
            if targets in self.track_name.values:
                track_loc = self.track_id.loc[self.track_name == targets]
                print(self.library.at[track_loc])
            else:
                print(" Track ID [", targets, "] not found in the library")
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
            print("Artist Result Found as Follow:")
            if self.artist_search_result is not None:
                # print([self.library.iloc[item] for item in self.artist_search_result.index.values])
                self.print(playlist=self.artist_search_result.index.values, list_print=False)
            else:
                print(" Artist [", targets, "] not found in the library")
            # TODO: Add Approximate Match with Dynamic Programming
            # Print Result for track name search
            print("Track Name Result Found as Follow:")
            if self.track_name_search_result is not None:
                # print([self.library.iloc[item] for item in self.track_name_search_result.index.values])
                self.print(playlist=self.track_name_search_result.index.values, list_print=False)
            else:
                print(" Track Name [", targets, "] not found in the library")

    # Covert all songs in a playlist to a wav file
    # playlist_to_audio(playlist, equalizer_type)
    # Input: playlist, equalizer_type
    # Output: local audio file
    def playlist_to_audio(self, playlist, equalizer_type, file_name, extension):
        print("Stream Info not verified, playlist_to_audio may not be working and/or as expected")
        self.mega_audio = []
        # Process equalizer_type length
        equalizer = equalizer_type * np.ceil(playlist.shape[0] / len(equalizer_type))
        # loop through playlist for individual songs
        for index in range(0, playlist.shape[0]):
            self.mega_audio.append(self.audio_action.default_process(track_id=playlist[index],
                                                                     equalizer_type=equalizer[index]))
        # Save the mega file
        # TODO: May Need Adjustments towards file parameters due to updated stream info
        # Solution1: General stream para
        AudioAction(track_id_library=self.track_id,
                    file_library=self.file_location,
                    audio=self.mega_audio).save_audio(file_name=file_name,
                                                      extension=extension,
                                                      use_original=True)


##############################################################
#   Function Prototype
##############################################################
def short_test():
    print("Testing short API")
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
    search_id = "20"
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


# IMPORTANT
# This is what is is supposed to perform with loading track stored in library
# But due to some technical issue that it is not implemented
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
    # !!! WARNING !!! Audio Action is not verified within the csv's file
    # !!! WARNING !!! Audio Modification has to be done in the fashion of fade/reverse then equalizing
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
    equalizer = ["Acoustic", "Vocal", "Piano"]
    lib.playlist_to_audio(playlist=playlist, equalizer_type=equalizer, file_name="mega_playlist", extension="wav")


##############################################################
#   Main Function
##############################################################
def main():
    print("Hello World!")
    # test_api()
    short_test()


##############################################################
#    Main Function Runner
##############################################################
if __name__ == "__main__":
    main()
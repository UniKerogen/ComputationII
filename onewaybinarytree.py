##############################################################
#   Libraries
##############################################################
import numpy as np
import csv
import random


##############################################################
#   Variable Definition
##############################################################


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
    def __init__(self, track_id, track_name=None, artist=None, album=None, file_location=None,
                 big=None, less=None):
        # Cargo
        self.track_id = track_id
        self.track_name = track_name
        self.artist = artist
        self.album = album
        self.file_location = file_location
        # Connector
        self.less = less
        self.big = big
        # Identifier

    # Print track_id
    # str()
    # input: None
    # Output: string of track_id
    def __str__(self):
        return str(self.track_id)

    # Print Node
    # print()
    # input: None
    # Output: None
    def print(self, show_file=False):
        if self.track_id > 0:
            print("    Track ID:", self.track_id)
            print("    Track Name:", self.track_name)
            print("    Artist:", self.artist)
            print("    Album:", self.album)
            if show_file:
                print("    File Location:", self.file_location)


# OneWayBinaryTree Class
# Create a OneWayBinaryTree and its data
# API Operation                     | Description
# OneWayBinaryTree(head)            | Initialize a binary tree
# len()                             | Return the count of elements in the tree
# count(node, counter)              | Counting sub-function
# str()                             | Print all elements in order
# access_node(node)                 | Print sub-function
# add(node, track_id)               | Add a song to the library
# delete(node, track_id)            | Delete a song from the library
# search_id(track_id)               | Search library for a song via track_id
class OneWayBinaryTree:
    # Initialize a OneWayBinaryTree
    # LinkedList(data)
    # Input: data
    # Output: None
    def __init__(self, head):
        self.head = head

    # print OneWayBinaryTree length
    # len()
    # Input: None
    # Output: length of the tree
    def __len__(self):
        counter = self.count(node=self.head, counter=0)
        return counter

    # count the tree sub function
    # count(node, counter)
    # Input: node, counter
    # Output: count result
    def count(self, node, counter=0):
        if not node:
            counter = self.count(node.less, counter=counter)
            counter += 1
            counter = self.count(node.big, counter=counter)
        return counter

    # direct print function
    # str()
    # Input: None
    # Output: Terminal Print
    def __str__(self):
        # print("Printing Library")
        # self.access_node(node=self.head)
        return "### Library Updated ###"

    # Access each node in the tree
    # access_node(node)
    # Input: Node
    # Output: Dependent
    def access_node(self, node):
        if node:
            self.access_node(node=node.less)
            node.print()
            print("")
            self.access_node(node=node.big)

    # Add a song to the library
    # add(track_id)
    # Input: track_id
    # Output: Dependent
    def add(self, current_node, track_id, track_name=None, artist=None, album=None, file_location=None):
        # Determine if track id input is valid
        if not track_id:
            print("Error(701): Unable to add to library due to invalid track id")
            return None
        # Determine if tree is empty
        if not current_node:
            return Node(track_id=track_id, track_name=track_name, artist=artist, album=album,
                        file_location=file_location)
        # Search to add in library
        if track_id < current_node.track_id:
            current_node.less = self.add(current_node=current_node.less, track_id=track_id,
                                         track_name=track_name, artist=artist, album=album, file_location=file_location)
        else:
            current_node.big = self.add(current_node=current_node.big, track_id=track_id,
                                        track_name=track_name, artist=artist, album=album, file_location=file_location)
        return current_node

    # Delete a node from the tree
    # delete(node, track_id)
    # Input: node, track_id
    # Output: Dependent
    def delete(self, node, track_id):
        # Determine if track id input is valid
        if not track_id:
            print("Error(702): Unable to delete track from library due to invalid track id")
            return None
        # End Case
        if not node:
            return None
        # Value Found
        if node.track_id == track_id:
            if node.less:
                # Find the biggest value of the subtree on the left
                less_biggest = node.less
                while less_biggest.big:
                    less_biggest = less_biggest.big
                # Attach the biggest value fo the subtree to bigger value
                less_biggest.big = node.big
                return node.less
            else:
                return node.big
        # In the case that it is not a match
        elif node.track_id > track_id:
            node.less = self.delete(node=node.less, track_id=track_id)
        else:
            node.big = self.delete(node=node.big, track_id=track_id)

        return node

    # Search the library for a specific track with track id
    # search_id(track_id)
    # Input: track_id
    # Output: node of the track_id if found | None if not found
    def search_id(self, node, track_id):
        # Determine if track id input is valid
        if not track_id:
            print("Error(703): Unable to delete track from library due to invalid track id")
            return None
        # Return value for not found and found
        if not node or node.track_id == track_id:
            return node
        # Looping
        if node.track_id < track_id:
            return self.search_id(node=node.big, track_id=track_id)
        else:
            return self.search_id(node=node.less, track_id=track_id)


# Class Library
# Create library
# API Operation                                             | Description
# Library(playlist_length)                                  | Create Library from csv
# add_track(playlist, add_track_id, add_track_location)     | Add track to a location in playlist
# print(playlist)                                           | Print playlist
class Library:
    def __init__(self, playlist_length, file_name="raw_track.csv", demo=False):
        # Initialize variables
        self.file_name = file_name
        self.library = OneWayBinaryTree(head=Node(track_id=0))
        self.demo = demo
        if self.demo:
            self.data_range = 175
        else:
            self.data_range = 155321
        # Load data into Library
        with open(self.file_name) as csv_file:
            tracks = csv.reader(csv_file, dialect='excel')
            index = 0
            for row in tracks:
                if demo:
                    if 0 < index < 10:
                        self.library.add(current_node=self.library.head,
                                         track_id=int(row[0]),
                                         track_name=row[37],
                                         artist=row[5],
                                         album=row[2],
                                         file_location=row[26])
                else:
                    if index > 0:
                        self.library.add(current_node=self.library.head,
                                         track_id=int(row[0]),
                                         track_name=row[37],
                                         artist=row[5],
                                         album=row[2],
                                         file_location=row[26])
                index += 1
        # Create a playlist
        self.playlist_length = playlist_length

    # Add a new song to library
    # lib_add(track_id)
    # Input: track_id
    # Output: None
    def lib_add(self, track_id, track_name=None, artist=None, album=None, file_location=None):
        if track_id > 0:
            # Pre-search library for existence
            result = self.library.search_id(node=self.library.head, track_id=track_id)
            if not result:
                self.library.add(current_node=self.library.head,
                                 track_id=track_id,
                                 track_name=track_name,
                                 artist=artist,
                                 album=album,
                                 file_location=file_location)
                print("Item (", track_id, ") has been added")
            else:
                print("This track_id (", track_id, ") exists in the library")
                result.print()
        else:
            print("Invalid input for track id")

    # Delete a song from the library
    # lib_delete(track_id)
    # Input: track_id
    # Output: None
    def lib_delete(self, track_id):
        if track_id > 0:
            # Pre-search library for existence
            result = self.library.search_id(node=self.library.head, track_id=track_id)
            if result:
                self.library.delete(node=self.library.head, track_id=track_id)
                print("Item (", track_id, ") has been deleted")
            else:
                print("This track_id (", track_id, ") does not exist in the library")
        else:
            print("Invalid input for track id")

    # Search library for a track via track_id
    # lib_search(track_id)
    # Input: track_id
    # Output: Terminal Print
    def lib_search(self, track_id):
        if track_id > 0:
            # Pre-search library for existence
            result = self.library.search_id(node=self.library.head, track_id=track_id)
            if result:
                print("This track id (", track_id, ") is found in the library")
                result.print()
            else:
                print("This track id (", track_id, ") is not found in the library")
        else:
            print("Invalid input for track id")

    def lib_print(self):
        print("Printing library")
        self.library.access_node(node=self.library.head)
        print(self.library)


##############################################################
#   Function Prototype
##############################################################
def test_api():
    # Create and Load a library
    lib = Library(playlist_length=10, file_name="raw_track_short.csv", demo=True)
    # Print Current Library
    lib.lib_print()
    # Add a song to library
    lib.lib_add(track_id=1,
                track_name="This is on You",
                artist="Maisie Peters",
                album="It's Your Bed Babe, It's Your Funeral - EP",
                file_location="/Users/kkgorgeous/Desktop/01_This_Is_On_You.m4a")

    lib.lib_add(track_id=40,
                track_name="Afterglow",
                artist="Taylor Swift",
                album="Lover",
                file_location="/Users/kkgorgeous/Desktop/15_Afterglow.m4a")

    lib.lib_add(track_id=100,
                track_name="Losing Me",
                artist="Gabrielle Aplin & JP Cooper",
                album="Dear Happy",
                file_location="/Users/kkgorgeous/Desktop/08_Losing_Me.m4a")

    lib.lib_add(track_id=134)
    lib.lib_add(track_id=-1)
    # Print Library
    lib.lib_print()
    # Search library for a song via Track ID
    lib.lib_search(track_id=100)
    lib.lib_search(track_id=101)
    lib.lib_search(track_id=-1)
    # Delete a song from Library
    lib.lib_delete(track_id=134)
    lib.lib_delete(track_id=46)
    lib.lib_delete(track_id=-1)
    lib.lib_delete(track_id=1000)
    # Print Library
    lib.lib_print()


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

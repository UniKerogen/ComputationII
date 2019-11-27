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

    # str()
    # creates a string with all the data from the list
    # inputs: none
    # returns: list in the form of a string
    def __str__(self):
        s = ''
        cur = self.head
        if cur is None:
            s += "EMPTY"
        while cur is not None:
            s += str(cur.track_id) + ' '
            cur = cur.next
        return s

    # Return shape
    # shape()
    # Input: None
    # Output: [length, height]
    def shape(self):
        return np.asarray([self.__len__(), 5])


# HashTable Class
# Create a Node and its data
# API Operation                     | Description
# Node(track_id)                    | Create Node
# insert(item)                      | Insert an item
# hash_function(key)                | Hashing Function
# str                               | Print track_id
class HashTable:
    # __init___(length)
    # constructor that makes an empty HashTable with length
    # inputs: numElements which is number of elements in Hash_Table
    # returns: none
    def __init__(self, length):
        self.length = length
        self.table = [None] * self.length
        index = 0
        for item in self.table:
            self.table[index] = LinkedList(None)
            index += 1
        self.n_data = 0

    # _hashFunc
    # hashing function
    # inputs: key
    # returns: location in hash table
    def hash_function(self, key):
        return key.track_id

    # insert(item)
    # inserts an item in the hash table
    # inputs: item - to insert
    # returns: none
    def insert(self, item):
        loc = int(self.hash_function(item))
        self.table[loc].append(item)

    # find(loc)
    # Find item at location
    # input: loc
    # output: item at loc
    def find(self, location):
        return self.table[location].head

    # str()
    # creates a string with all the data from the table
    # inputs: none
    # returns: table in the form of a string
    def __str__(self):
        s = ''
        i = 0
        for x in self.table:
            s += "Data at index " + str(i) + " is \n"
            s += str(self.table[i])
            s += "\n"
            i = i + 1
        return s

    # __getitem__(item)
    # Obtain Linked Note at location
    # input: location
    # output: node at location
    def __getitem__(self, item):
        if 0 < item < self.length:
            return self.table[item].head.track_id
        else:
            print("Error(900): Index Out of Range or not in range")
            exit(900)


# Class Library
# Create library
# API Operation                                             | Description
# Library(playlist_length)                                  | Create Library from csv
# add_track(playlist, add_track_id, add_track_location)     | Add track to a location in playlist
# print(playlist)                                           | Print playlist
class Library:
    def __init__(self, playlist_length, file_name="raw_track.csv", repeat=False):
        # Load Library
        self.file_name = file_name
        self.data_range = 175  # 155321
        self.library = HashTable(self.data_range)
        with open(self.file_name) as csv_file:
            tracks = csv.reader(csv_file, dialect='excel')
            index = 0
            for row in tracks:
                if index > 0:
                    new_node = Node(track_id=row[0],
                                    track_name=row[37],
                                    artist=row[5],
                                    album=row[2],
                                    file_location=row[26])
                    self.library.insert(item=new_node)
                index += 1
        # Check Playlist Length
        self.playlist_length = playlist_length
        if self.playlist_length > self.data_range:
            print("## Length Out of Range ##")
            self.playlist_length = self.data_range
        else:
            self.playlist_length = self.playlist_length
        # Generate Playlist
        random_list = np.zeros(self.playlist_length)
        index = 0
        while index <= self.playlist_length - 1:
            temp_num = random.randint(0, self.data_range - 1)
            # Check if exists
            if not repeat:
                exist = 0
                for index2 in range(0, self.playlist_length):
                    if temp_num == int(random_list[index2]):
                        exist = 1
                if exist == 0 and self.library.find(temp_num) is not None:
                    random_list[index] = temp_num
                    index += 1
                else:
                    index = index
            else:
                random_list[index] = temp_num
                index += 1
        # Push playlist info
        self.playlist = LinkedList(None)
        for item in random_list:
            track_id = int(item)
            self.playlist.append(track_id=self.library[track_id].track_id,
                                 track_name=self.library[track_id].track_name,
                                 artist=self.library[track_id].artist,
                                 album=self.library[track_id].album,
                                 file_location=self.library[track_id].file_location)

    # Add a track to the playlist
    # add_track(playlist, add_track_id, add_track_location)
    # Input: playlist, add_track_id, add_track_location
    # Output: modified playlist
    def add_track(self, playlist, add_track_id, add_track_location):
        outer_range = len(playlist)
        # Find the corresponding track info
        if self.library[add_track_id] is not None:
            if add_track_location > outer_range or add_track_location < 1:
                print("Warning(901): Add Out of Index")
                add_loc = outer_range
            else:
                add_loc = add_track_location - 1
            # Add to playlist
            pre_track = playlist.find_nth(n=add_loc)
            playlist.insert_after(pre_track_id=pre_track,
                                  track_id=add_track_id,
                                  track_name=self.library[add_track_id].track_name,
                                  artist=self.library[add_track_id].artist,
                                  album=self.library[add_track_id].album,
                                  file_location=self.library[add_track_id].file_location)
            return LinkedList(head=playlist.head)
        else:
            print("Warning(902): Item not found in library")
            return LinkedList(head=playlist.head)

    # Print the current playlist
    # print(playlist)
    # Input: playlist
    # Output: None
    def print(self, playlist):
        print("Printing Current Playlist")
        playlist.print_list()
        print("")


##############################################################
#   Function Prototype
##############################################################
def test_api():
    # Create Library
    lib = Library(file_name="raw_track_short.csv", playlist_length=10)
    # Obtain Playlist
    playlist = lib.playlist
    # Print Playlist
    lib.print(playlist=playlist)
    # Add new song to playlist
    playlist = lib.add_track(playlist=playlist, add_track_id=-1, add_track_location=5) #Cory tried 154, -1 pass, -1, 5 fail
    # Print playlist
    lib.print(playlist)


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

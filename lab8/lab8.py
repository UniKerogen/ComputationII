##############################################################
#   Libraries
##############################################################
import csv
import os
import time
import sys
sys.setrecursionlimit(200000)
import random


##############################################################
#   Variable Definition
##############################################################
BLACK = "BLACK"
RED = "RED"
EMPTY = "EMPTY"


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
                 right=None, left=None, parent=None,
                 color=None):
        # Cargo
        self.track_id = track_id
        self.track_name = track_name
        self.artist = artist
        self.album = album
        self.file_location = file_location
        # Connector
        self.left = left
        self.right = right
        self.parent = parent
        # Identifier
        self.color = color

    # Iteration Control
    # iter(self)
    # Input: None
    # Output: The iteration of the tree
    def __iter__(self):
        # Left Branch
        if self.left.color is not EMPTY:
            yield from self.left
        # Self Branch
        yield self.track_id
        # Right Branch
        if self.right.color is not EMPTY:
            yield from self.right

    # str output for the node
    # str()
    # input: None
    # Output: string of track_id and color of the node
    def __str__(self):
        return str(self.track_id) + " " + str(self.color)

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

    # Print Node with all information
    # print_all()
    # Input: None
    # Output: Terminal Print
    def print_all(self):
        if self.track_id > 0:
            print("    ### Cargo ###")
            print("    Track ID:", self.track_id)
            print("    Track Name:", self.track_name)
            print("    Artist:", self.artist)
            print("    Album:", self.album)
            print("    File Location:", self.file_location)
            print("    ### Connection ###")
            print("    Connection   [LEFT]:", self.left)
            print("    Connection  [RIGHT]:", self.right)
            print("    Connection [PARENT]:", self.parent)
            print("    ### Identifier ###")
            print("    Color:", self.color)

    # Count children of the node
    # children_count():
    # Input: None
    # Output: count number
    def children_count(self):
        if self.color is EMPTY:
            return 0
        return sum([int(self.left != EMPTY), int(self.right != EMPTY)])

    # determine if it has children
    # has_children()
    # Input: None
    # Output: True/False
    def has_children(self):
        return bool(self.children_count())

    # get its children
    # get_children()
    # Input: None
    # OutputL Terminal Output
    def get_children(self, more_detail=False):
        # Print left child
        if self.left != EMPTY:
            print("Connection [LEFT] :", self.left.track_id)
            if more_detail:
                self.left.print(show_file=False)
        else:
            print("Connection [LEFT] : None")
        # Print right child
        if self.right != EMPTY:
            print("Connection [RIGHT]:", self.right.track_id)
            if more_detail:
                self.right.print(show_file=False)
        else:
            print("Connection [Right]: None")


# RedBlackTree Class
# Create Red Black Tree and its data
# API Operation                     | Description
# RedBlackTree()                    | Initialize a Red Black Tree
# insert(track_id)                  | insert a new node with its track id to the tree
# search(track_id)                  | search tree for a specific track id
class RedBlackTree:
    # Initialize the red black tree
    def __init__(self):
        self.count = 0
        self.root = None
        self.empty_block = Node(track_id=None, color=BLACK, parent=None)

    # Obtain the full extent of the tree
    def __iter__(self):
        if not self.root:
            return list()
        yield from self.root.__iter__()

    # {INTERNAL FUNCTION} Determine Relationship between node and its parent's family
    # update_parent_node(node, new_parent, old_child)
    # Input: node, its new_parent, its new_parent's old_child
    # Output: updated node
    def update_parent_node(self, node, new_parent, old_child):
        node.parent = new_parent
        # Check if new_parent is not Empty case
        if new_parent.track_id:
            if new_parent.track_id > old_child.track_id:
                new_parent.left = node
            else:
                new_parent.right = node
        # new_parent is Empty case
        else:
            self.root = node

    # {INTERNAL FUNCTION} Rotation Motion
    # rotate(rotation, node, parent, grandparent)
    # Input: rotation [L|R], node, parent (aimed connection point), grandparent (current connection point)
    # Output: Rotated Tree Branch
    def rotate(self, rotation, node, parent, grandparent, recolor=False):
        # Obtain Information regarding great grandparent
        great_grandparent = grandparent.parent
        # Rotation
        self.update_parent_node(node=parent, new_parent=great_grandparent, old_child=grandparent)
        # Left Rotation
        if rotation == "L":
            # Old Family
            old_sibling = parent.left
            # New Family
            parent.left = grandparent
            grandparent.parent = parent
            grandparent.right = old_sibling
            old_sibling.parent = grandparent
        elif rotation == "R":
            # Old Family
            old_sibling = parent.right
            # New Family
            parent.right = grandparent
            grandparent.parent = parent
            grandparent.left = old_sibling
            old_sibling.parent = grandparent
        else:
            print("Error(802): Unable to determine rotation direction")
            exit(802)
        # Coloring Option
        if recolor:
            parent.color = BLACK
            node.color = RED
            grandparent.color = RED

    # Insert Function
    # insert(track_id)
    # Input: track_id
    # Output: New Tree
    def insert(self, track_id, track_name=None, artist=None, album=None, file_location=None):
        new_node = Node(track_id=track_id, track_name=track_name, artist=artist, album=album, file_location=file_location)
        self.tree_insert(node=new_node)
        self.count += 1

    # {INTERNAL FUNCTION} Insert into Tree Function
    # tree_insert(node)
    # Input: node
    # Output: New Tree
    def tree_insert(self, node):
        # Control Variable
        skip = False
        if_root = False
        insert_previous_node = self.empty_block
        loop_node = self.root
        if not self.root:
            loop_node = self.empty_block
        # Find the parent of the new node
        while loop_node is not self.empty_block:
            insert_previous_node = loop_node
            if node.track_id < loop_node.track_id:
                loop_node = loop_node.left
            elif node.track_id > loop_node.track_id:
                loop_node = loop_node.right
            else:
                print("Error(801): This track id already exists, unable to insert.")
                loop_node.print()
                skip = True
                break
        # Post Location Found Assignment
        if skip:
            return
        # Assign the parent of the new node
        node.parent = insert_previous_node
        # Relationship Assignment
        if insert_previous_node == self.empty_block:
            node.color = BLACK
            self.root = node
            if_root = True
        elif node.track_id < insert_previous_node.track_id:
            insert_previous_node.left = node
        else:
            insert_previous_node.right = node
        # Leaf of the new node
        node.left = self.empty_block
        node.right = self.empty_block
        if not if_root:
            node.color = RED
            # Run Color Fix Function
            self.insert_fix(node)

    # {INTERNAL FUNCTION} Color Fix after Insert
    # insert_fix(node)
    # input: node
    # Output: Depends
    def insert_fix(self, node):
        # Obtain Information Regarding Self & Parent
        parent = node.parent
        self_id = node.track_id
        # No Fix Needed Case
        # FailSafe | Root | Already Balanced
        if (parent is None) or (parent.parent is None) or (node.color != RED or parent.color != RED):
            return
        # Obtain Information Regarding Grandparents
        grandparent = parent.parent
        # Connection between node and parent
        self_side = "L" if self_id < parent.track_id else "R"
        # Determine the uncle of the node
        uncle_side = "L" if parent.track_id < grandparent.track_id else "R"
        uncle = grandparent.right if uncle_side == "L" else grandparent.left
        two_sides = self_side + uncle_side
        # Determine Rotation | When uncle is BLACK or Empty [OR] Red
        if uncle == self.empty_block or uncle.color == BLACK:
            if two_sides == "LL":
                self.rotate(rotation="R", node=node, parent=parent, grandparent=grandparent, recolor=False)
            elif two_sides == "LR":
                # Switch place with node and parent
                self.rotate(rotation="R", node=self.empty_block, parent=node, grandparent=parent, recolor=False)
                self.rotate(rotation="L", node=parent, parent=node, grandparent=grandparent, recolor=True)
            elif two_sides == "RL":
                # Switch place with node and parent
                self.rotate(rotation="L", node=self.empty_block, parent=node, grandparent=parent, recolor=False)
                self.rotate(rotation="R", node=parent, parent=node, grandparent=grandparent, recolor=True)
            elif two_sides == "RR":
                self.rotate(rotation="L", node=node, parent=parent, grandparent=grandparent, recolor=True)
            else:
                print("Error(803): Unable to determine side connection of the previous two family members")
                exit(803)
        else:
            self.recolor(node=grandparent)

    # {INTERNAL FUNCTION} Recolor certain node and try to fix again
    # recolor(node)
    # Input: node
    # Output: Depends
    def recolor(self, node):
        node.right.color = BLACK
        node.left.color = BLACK
        if node != self.root:
            node.color = RED
        self.insert_fix(node=node)

    # Search for node with track_id
    # search(track_id)
    # Input: track_id
    # Output: Terminal Print
    def search(self, track_id, print_node=False):

        # Sub function for search looping
        # find(current_node)
        # Input: current_node
        # Output: a node
        def find(current_node):
            if current_node is None or current_node == self.empty_block:
                return None
            if track_id < current_node.track_id:
                return find(current_node=current_node.left)
            elif track_id > current_node.track_id:
                return find(current_node=current_node.right)
            else:
                return current_node

        # Determine if track id input is valid
        if not track_id:
            print("Error(804): Unable to delete track from library due to invalid track id")
            return None
        # Return value for not found and found
        node_found = find(current_node=self.root)
        if print_node:
            node_found.print()
        return node_found

    # find the minimum value of the tree
    # minimum()
    # Input: None
    # Return: the minimum value of the tree
    def minimum(self):
        # Determine if tree is empty
        if self.root is None:
            return None
        # Setup for search & find
        current_node = self.root
        min_value = self.root.track_id
        while current_node != self.empty_block:
            if current_node.track_id < min_value:
                min_value = current_node.track_id
            current_node = current_node.left
        return min_value

    # find the maximum value of the tree
    # maximum()
    # Input: None
    # Output: the maximum value of the tree
    def maximum(self):
        # Determine if tree is empty
        if self.root is None:
            return None
        # Setup for search & find
        current_node = self.root
        max_value = self.root.track_id
        while current_node != self.empty_block:
            if current_node.track_id > max_value:
                max_value = current_node.track_id
            current_node = current_node.right
        return max_value


# Library Class
#
class Library:
    def __init__(self, playlist_length, file_name="raw_track.csv", demo=False):
        # Initialize variables
        self.file_name = file_name
        if not os.path.isfile(self.file_name):
            print("Error(800): Unable to find file")
            exit(800)
        self.library = RedBlackTree()
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
                        self.library.insert(track_id=int(row[0]),
                                            track_name=row[37],
                                            artist=row[5],
                                            album=row[2],
                                            file_location=row[26])
                else:
                    if 0 < index < 5000:
                        self.library.insert(track_id=int(row[0]),
                                            track_name=row[37],
                                            artist=row[5],
                                            album=row[2],
                                            file_location=row[26])
                index += 1
        # Range of the library
        self.min = self.library.minimum()
        self.max = self.library.maximum()
        # Create a playlist
        self.playlist_length = playlist_length

    # Add a new song to library
    # lib_add(track_id)
    # Input: track_id
    # Output: None
    def lib_add(self, track_id, track_name=None, artist=None, album=None, file_location=None):
        if track_id > 0:
            # Pre-search library for existence
            result = self.library.search(track_id=track_id)
            if not result:
                self.library.insert(track_id=track_id,
                                    track_name=track_name,
                                    artist=artist,
                                    album=album,
                                    file_location=file_location)
                print("Item (", track_id, ") has been added")
                # Rebuild Region
                self.min = self.library.minimum()
                self.max = self.library.maximum()
            else:
                print("This track_id (", track_id, ") exists in the library")
                result.print()
        else:
            print("Invalid input for track id")

    # Search library for a track via track_id
    # lib_search(track_id)
    # Input: track_id
    # Output: Terminal Print
    def lib_search(self, track_id, print_data=True):
        if track_id > 0:
            # Pre-search library for existence
            result = self.library.search(track_id=track_id)
            if result:
                if print_data:
                    print("This track id (", track_id, ") is found in the library")
                    result.print()
            else:
                if print_data:
                    print("This track id (", track_id, ") is not found in the library")
        else:
            if print_data:
                print("Invalid input for track id")

    # Print the library
    # lip_print()
    # Input: None
    # OutputL Terminal Print
    def lib_print(self):
        print(self.library)


##############################################################
#   Function Prototype
##############################################################
def test_api(file_name):
    # Create and Load a library
    lib = Library(playlist_length=10, file_name=file_name, demo=False)
    # Search 
    start_time = time.time()
    for search_incident in range(0, 1000):
        lib.lib_search(track_id=random.randint(lib.library.minimum(), lib.library.maximum()), print_data=False)
    end_time = time.time()
    print(end_time - start_time)  # seconds
    # retrun (end_time - start_time)
        


##############################################################
#   Main Function
##############################################################
def main(argv):
    # Determine File
    if argv == "rds":
        file_name = "raw_track_short_rd.csv"
    elif argv == "rda":
        file_name = "raw_tracks_rd.csv"
    elif argv == "s":
        file_name = "raw_track_short.csv"
    elif argv == "a":
        file_name = "raw_tracks.csv"
    else:
        print("Error(806): Unable to determine the file name")
        exit(806)
    
    test_api(file_name)



##############################################################
#    Main Function Runner
##############################################################
if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Error(805): Unable to run the scrip due to insufficient input")
        print("      Usage: python3 lab8.py [FIlE_NAME_ABBR]")
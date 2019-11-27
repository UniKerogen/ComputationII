# Course: ECE 3822
# Lab: 3
# Date: 9/11/2019
# Username: kuang
# Name: Kuang Jiang
# Description: Lab3 card search file
# File Name: lab3_cardsearch.py

##############################################################
#   Libraries
##############################################################
import os
import sys
import random
import numpy as np


##############################################################
#   Function Prototype
##############################################################
# Custom Card Search Function
# Perform a card search
# Input data, target
# Output: result[mid, check]
def card_search(data, target):
    low = 0
    high = 25
    mid = (low + high) // 2
    check = 0
    while low <= high:
        check += 1
        if target[0] > data[mid][0]:
            low = mid + 1
        elif target[0] < data[mid][0]:
            high = mid - 1
        elif target[0] == data[mid][0]:
            if target[1] > data[mid][1]:
                low = mid + 1
            elif target[1] < data[mid][1]:
                high = mid - 1
            elif target[1] == data[mid][1]:
                # print("Target Found at location", mid)
                return [mid, check]
        mid = (low + high) // 2
    # print("Search Compete and Target not Found: -1")
    return [-1, check]
            

# Intilze Set
# Obtained from sample file
# example program generating an 13x52 array for a deck of cardsas well as generating a random sample of that deck to be used for Lab 3
# input: no input
# output: hand
def start():
    #start with suit array
    suit_array1 = np.ones(13)
    suit_array2 = np.ones(13)*2
    suit_array3 = np.ones(13)*3
    suit_array4 = np.ones(13)*4
    suit_array = np.concatenate((suit_array1,suit_array2,suit_array3,suit_array4))
    # print(suit_array)
    
    #make rank array
    rank_array1to13=np.linspace(1,13,13)
    rank_array=np.concatenate((rank_array1to13,rank_array1to13,rank_array1to13,rank_array1to13))
    # print(rank_array)
    
    #make deck array
    deck_array=np.stack((suit_array,rank_array))
    # print("deck array transposed before sample")
    # print(deck_array.T)
    deck_array=deck_array.T
    
    #now sample at random which 26 cards to pick, run this code to generate a hand
    numCardsToPick=26
    hand=np.delete(deck_array,random.sample(range(52),numCardsToPick),axis=0)
    # print("hand")
    # print(hand)
    return hand
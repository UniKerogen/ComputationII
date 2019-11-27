# Course: ECE 3822
# Lab: 3
# Date: 9/11/2019
# Username: kuang
# Name: Kuang Jiang
# Description: Lab3_bsearch file
# File Name: lab3._bsearch.py

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
# Generate the set
# input: length of the set
# Output: the set
def set_generation(length, data_range):
    # Initialize set
    data_set = np.zeros(length)
    # print(data_set)
    # Start Index the set
    index = 0
    while index <= length - 1:
        # print("In Index", index)
        temp_num = random.randint(1, data_range)
        # print(" *Get Num", temp_num)
        # Check if exists
        exist = 0
        for index2 in range(0, length):
            if temp_num == int(data_set[index2]):
                exist = 1
        if exist == 0:
            data_set[index] = temp_num
            index += 1
        else:
            index = index
    # print(data_set)
    return np.sort(data_set)
    
    
# Bindary Search Function
# Perform a binary search
# Input: data_set, target
# Output: result[mid, check]
def binary_search(data, target):
    low = 0
    high = 25
    mid = target // 2
    check = 0
    while low <= high:
        check += 1
        if mid == target:
            # print("Target Card Found at location", mid)
            return [mid, check]
        elif mid < target:
            high = mid - 1
        elif mid > target:
            low = mid + 1
        mid = (low + high) // 2
    # print("Search Competed and Target not Found: -1")
    return [-1, check]
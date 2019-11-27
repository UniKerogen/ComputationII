# Course: ECE 3822
# Lab: 3
# Date: 9/11/2019
# Username: kuang
# Name: Kuang Jiang
# Description: Lab3 file
# File Name: lab3.py

##############################################################
#   Libraries
##############################################################
import os
import sys
import random
import numpy as np
from lab3_bsearch_Jiang import *
from lab3_cardsearch_Jiang import *

##############################################################
#   Variable Definition
##############################################################


##############################################################
#   Function Prototype
##############################################################
# Loop Function
# Loop calcualition for 1000 times and record the result
# Input: max_loop_number
# Output: result[result1, result2]
def circling(max_loop_number):
    for loop in range(0, max_loop_number):
        # print(loop)
        if loop == 0:
            # Start No.1
            data_set1 = set_generation(length=26, data_range=52)
            # print(data_set1)
            result1 = np.asarray(binary_search(data=data_set1, target=random.randint(1, 52)))
            
            # Start No.2
            data_set2 = start()
            target = [random.randint(1, 4), random.randint(1, 13)]
            result2 = np.asarray(card_search(data=data_set2, target=target))
        else:
            data_set1 = set_generation(length=26, data_range=52)
            result1 = np.row_stack((result1, np.asarray(binary_search(data=data_set1, target=random.randint(1, 52)))))
            data_set2 = start()
            target = [random.randint(1, 4), random.randint(1, 13)]
            result2 = np.row_stack((result2, np.asarray(card_search(data=data_set2, target=target))))
    
    sum1 = 0
    sum2 = 0
    for loop in range(0, result1.shape[0]):
        sum1 += result1[loop][1] 
        sum2 += result2[loop][1]
    
    avg1 = sum1 / result1.shape[0]
    avg2 = sum2 / result2.shape[0]
    
    return[avg1, avg2]
    
    
##############################################################
#   Main Function
##############################################################
def main():
    print("Hello World!")
    [avg1, avg2] = circling(10000)
    print("Average Check Rate for BSearch is ", avg1)
    print("Average Check Rate for CSearch is ", avg2)
    
    
##############################################################
#    Main Function Runner
##############################################################
if __name__ == "__main__":
    main()

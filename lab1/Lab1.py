# Course: ECE 3822
# Lab: 1
# Date: 8/30/2019
# Username: kuang
# Name: Kuang Jiang
# Description: Start-up Project
# File Name: Lab1.py

##############################################################
#   Libraries
##############################################################
import sys
import os


##############################################################
#   Variable Definition
##############################################################


##############################################################
#   Function Prototype
##############################################################
##############################################################
# random_number(x, y, z)
# This function is used to show I can use python and debugger
# Input: x, y, z
# Output: No Return Value
def random_number(x, y, z):
    x = 10
    y = 11
    z = 30
    
    x = x + y
    y = y + z
    z = z + x
    
    x = 10 * y
    y = z * 2
    z = y * 10
    
    print("x = ", x)
    print("y = ", y)
    print("z = ", z)
    


##############################################################
#   Main Function
##############################################################
def main():
    print("Hello World!")
    random_number(1, 2, 3)


##############################################################
#    Main Function Runner
##############################################################
if __name__ == "__main__":
    main()

# Course: ECE 3822
# Lab: 4
# Date: 9/11/2019
# Username: kuang
# Name: Kuang Jiang
# Description: Lab4 file
# File Name: lab4.py

##############################################################
#   Libraries
##############################################################
import math

##############################################################
#   Variable Definition
##############################################################


##############################################################
#   Class Prototype
##############################################################
# Point Class
# Create and store a point
# API Operation     | Description
# Point(x, y)       | a New pont set at [x, y]
# a.distanceTo(b)   | calculate distance betwen point a and b
# str               | Print the current point location, a string representation
# add               | Add point a and b together and return the result
class Point():
    # init(x, y)
    # This function is used to Initialize the class with its sub varairable x & y
    # Input: geo-point x & y which are both numbers
    # Output: None
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    # str()
    # This function return string value of current class value x & y
    # Input: None
    # Output: formatted string of point
    def __str__(self):
        return f"Point is [{self.x}, {self.y}]\n"
    
    # distanceTo(b)
    # This functio calculate the distance form point b to point a
    # Input: point b, which is a class of Point
    # Output: distance from a to b
    def distanceTo(self, b):
        distance = (self.x - b.x)**2 + (self.y - b.y)**2
        return math.sqrt(distance)
    
    # add(b)
    # This function add point a and b together x, y respectively
    # Input: point b
    # Output: 2D array of the result
    def __add__(self, b):
        point = [self.x + b.x, self.y + b.y]
        return point
        

##############################################################
#   Function Prototype
##############################################################


##############################################################
#   Main Function
##############################################################
def main():
    print("Hello World!")
    # Initialize point a
    a = Point(1, 2)
    # Initialize point b
    b = Point(2, 3)
    # Calculate and print distance between a and b
    print(a.distanceTo(b))
    # Print point of as
    print(a)
    


##############################################################
#    Main Function Runner
##############################################################
if __name__ == "__main__":
    main()
